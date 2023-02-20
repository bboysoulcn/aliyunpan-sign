import requests
import json
import schedule
import time
import hmac
import hashlib
import base64
import urllib.parse
from environs import Env


def send_msg(msg):
    timestamp = str(round(time.time() * 1000))
    secret = ding_secret
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    body = {
        "msgtype": "markdown",
        "markdown": {
            "title": "提醒",
            "text": msg
        },
        "at": {
            "isAtAll": "true"
        }
    }
    dingding_url = dingding_base_url + "&timestamp=" + timestamp + "&sign=" + sign
    requests.post(dingding_url, json.dumps(body), headers=headers)


def sign(refresh_token):
    update_token_url = "https://auth.aliyundrive.com/v2/account/token"
    signin_url = "https://member.aliyundrive.com/v1/activity/sign_in_list"

    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps({
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    })
    req = requests.Session()
    resp = req.post(update_token_url, data=data, headers=headers).text
    access_token = json.loads(resp)['access_token']
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    resp = req.post(signin_url, data=data, headers=headers)
    result = json.loads(resp.text)['success']
    if result:
        send_msg("阿里云盘签到成功")
    else:
        send_msg("阿里云盘签到失败")
    return result


if __name__ == '__main__':
    env = Env()
    ding_secret = env.str('DING_SECRET')
    dingding_base_url = env.str('DINGDING_BASE_URL')
    refresh_token_list = env.list('REFRESH_TOKEN_LIST')
    schedule_time = env.str('TIME')
    for refresh_token in refresh_token_list:
        schedule.every().day.at(schedule_time).do(sign, refresh_token)
    print("应用启动成功")
    while True:
        schedule.run_pending()
        time.sleep(1)

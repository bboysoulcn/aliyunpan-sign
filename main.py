import requests
import json
import schedule
import time
import hmac
import hashlib
import base64
import urllib.parse
from environs import Env
from loguru import logger


def send_telegram(msg):
    token = bot_token
    data = {
        "chat_id": chat_id,
        "text": msg
    }
    url = "https://api.telegram.org/bot" + token + "/sendMessage"
    req = requests.session()
    result = json.loads(req.post(url, data=data).text)['ok']
    return result


def send_dingdingmsg(msg):
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


def aliyundrive_sign(token):
    update_token_url = "https://auth.aliyundrive.com/v2/account/token"
    signin_url = "https://member.aliyundrive.com/v1/activity/sign_in_list"

    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps({
        'grant_type': 'refresh_token',
        'refresh_token': token
    })
    req = requests.Session()
    resp = json.loads(req.post(update_token_url, data=data, headers=headers).text)
    if "access_token" in resp:
        access_token = resp['access_token']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
        resp = req.post(signin_url, data=data, headers=headers)
        result = json.loads(resp.text)['success']

        if result:
            send_msg("阿里云盘签到成功")
            logger.info("阿里云盘签到成功")
        else:
            send_msg("阿里云盘签到失败")
    else:
        logger.error('token 已失效请更新环境变量重新启动容器')


def msg_channel_handle(msg_channel):
    if msg_channel == "dingding":
        return send_dingdingmsg
    if msg_channel == "telegram":
        return send_telegram


if __name__ == '__main__':
    env = Env()
    bot_token = env.str('BOT_TOKEN')
    chat_id = env.str('CHAT_ID')

    ding_secret = env.str('DING_SECRET')
    dingding_base_url = env.str('DINGDING_BASE_URL')
    refresh_token_list = env.list('REFRESH_TOKEN_LIST')

    schedule_time = env.str('TIME')

    msg_channel = env.str('MSG_CHANNEL')
    send_msg = msg_channel_handle(msg_channel)
    for refresh_token in refresh_token_list:
        schedule.every().day.at(schedule_time).do(aliyundrive_sign, refresh_token)
        # schedule.every(3).seconds.do(aliyundrive_sign, refresh_token)
    logger.info("应用启动成功")
    while True:
        schedule.run_pending()
        time.sleep(1)

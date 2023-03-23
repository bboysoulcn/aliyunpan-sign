# 阿里云盘自动签到脚本

一般不会弃坑，有问题提issue

### todo

- 是不是需要告警
- telegram 告警

### 获取 refresh_token

1. 网页登录阿里云盘官网 https://www.aliyundrive.com/drive
2. 按F12，进入开发者工具模式，在顶上菜单栏点 Application ，然后在左边菜单找到 Local storage 下面的 https://www.aliyundrive.com 这个域名，点到这个域名会看到有一个 token 选项，再点 token ，就找到 refresh_token 了

### 配置环境变量

编辑env文件

- DING_SECRET: 钉钉机器人的secret
- DINGDING_BASE_URL: 钉钉机器人baseurl
- REFRESH_TOKEN_LIST: 多个refresh token的话REFRESH_TOKEN_LIST以逗号分开，比如`REFRESH_TOKEN_LIST="token1,token2"`
- TIME: 脚本运行的时间
- BOT_TOKEN: telegram机器人的token
- CHAT_ID: telegram的会话id
- MSG_CHANNEL: 发送消息的通道，目前只支持[dingding,telegram]

### 启动

`docker-compose  up -d `

### 最后

欢迎关注我的博客[www.bboy.app](https://www.bboy.app/)

Have Fun


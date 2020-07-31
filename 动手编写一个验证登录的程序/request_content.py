import requests

# requests会把用户名和密码放在请求头的Authorization参数中
# r = requests.get('http://127.0.0.1:5000/login', auth=('erics', '123456'))
# print(r.text)  # ZXJpY3M6MC40NzI1OTkwNTMzNjA3NDgyNjoxNTk2MTI3MjE5LjczMDU0OTM=

token = 'ZXJpY3M6MC40NzI1OTkwNTMzNjA3NDgyNjoxNTk2MTI3MjE5LjczMDU0OTM='
# GET /test?token=ZXJpY3M6MC44NjkxMjI0MjQ4NjAzMTY4OjE1OTYxMjcxMDcuNjgyNzU3MQ==
r = requests.get('http://127.0.0.1:5000/test', params={'token': token})
print(r.text)
"""
验证成功！
"""
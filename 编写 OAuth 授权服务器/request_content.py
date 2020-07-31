import requests

r = requests.get('http://127.0.0.1:5000/client/login')
print(r.text)  # Please login!
print(r.history)  # [<Response [302]>]
print(
    r.url)  # http://127.0.0.1:5000/oauth?response_type=code&client_name=123456&redirect_uri=http://127.0.0.1:5000/client/passport
uri_login = r.url.split('?')[0] + '?user=erics&pwd=123456'
print(uri_login)  # http://127.0.0.1:5000/oauth?user=erics&pwd=123456
r2 = requests.get(uri_login)
print(r2.text)  # MTIzNDU2OjAuODIwODcyMjI5MzA3MTM2ODoxNTk2MTgxNDA2Ljg2MDgzNw==
print(r2.history)  # [<Response [302]>, <Response [302]>]
r = requests.get('http://127.0.0.1:5000/test', params={'token': r2.text})
print(r.text)
"""
Please login!
[<Response [302]>]
http://127.0.0.1:5000/oauth?response_type=code&client_name=123456&redirect_uri=http://127.0.0.1:5000/client/passport
http://127.0.0.1:5000/oauth?user=erics&pwd=123456
MTIzNDU2OjAuNzMwMTkzNzc3Nzk4ODk5NToxNTk2MTg0OTQzLjg1MjQ3MTY=
[<Response [302]>, <Response [302]>]
验证成功！
"""

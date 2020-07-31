from flask import Flask, request, redirect
import base64, random, time

app = Flask(__name__)
# 键是用户名，值用于存储用户密码和token
users = {
    'erics': ['123456']
}
redirect_uri = 'http://127.0.0.1:5000/client/passport'
# 为用户注册账号并添加到users字典中
client_name = '123456'
users[client_name] = []
# 授权服务器需要保存重定向uri
oauth_redirect_uri = []
auth_code = {}


def generate_token(user_name):
    """
    生成token
    :param user_name:
    :return:token <class 'bytes'>
    """
    # 通过base64加密token(token由用户名、随机数、时间戳+7200s组成并通过冒号连接在一起)
    token = base64.b64encode(
        str.encode(':'.join([str(user_name), str(random.random()), str(time.time() + 7200)])))  # str.encode()：字符串转字节
    print(token)  # b'ZXJpY3M6MC4xOTgyMTg1NTE3NDk1MjY2MzoxNTk2MTI0MDI4Ljc1NzgwODQ='
    # 将加密后的token添加到用户(键)对应的列表中（第二个值，PS：第一个是用户的密码）
    users[user_name].append(str(token, encoding='utf-8'))
    print(type(token))  # <class 'bytes'>
    return token


def verify_token(token):
    """
    验证token
    :param token:
    :return:
    """
    print(type(token))  # ZXJpY3M6MC40NzI1OTkwNTMzNjA3NDgyNjoxNTk2MTI3MjE5LjczMDU0OTM= <class 'str'>
    # 解密token
    _token = base64.b64decode(token)  # <class 'str'>
    print(_token)  # b'erics:0.41836337072512586:1596125759.8535287'
    _token = str(_token, encoding='utf-8')
    print(_token)  # erics:0.41836337072512586:1596125759.8535287
    # _token.split(':')[0]获取的是用户名，users.get(_token.split(':')[0])[-1]是通过这个用户名获取之前生成好的token
    if not users.get(_token.split(':')[0])[-1] == token:
        return -1
    # 如果token一致，验证是否过期
    if float(_token.split(':')[-1]) >= time.time():  # type(time.time()):float
        return 1
    else:
        return 0


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录
    :return:
    """
    """
    print(request.headers['Authorization'])  # Basic ZXJpY3M6MTIzNDU2
    print(request.headers['Authorization'].split(' '))  # ['Basic', 'ZXJpY3M6MTIzNDU2']
    print(request.headers['Authorization'].split(' ')[-1])  # ZXJpY3M6MTIzNDU2
    print(base64.b64decode(request.headers['Authorization'].split(' ')[-1]))  # b'erics:123456'
    print(bytes.decode(base64.b64decode(request.headers['Authorization'].split(' ')[-1])))  # erics:123456
    print(str(base64.b64decode(request.headers['Authorization'].split(' ')[-1]), encoding='utf-8'))  # erics:123456
    """
    # 解密之后得到的是字节类型（加密得到的也是字节），这里字节转成字符串是为了与用户名和密码进行比较
    user_name, pwd = str(base64.b64decode(request.headers['Authorization'].split(' ')[-1]), encoding='utf-8').split(':')
    print(user_name, pwd)  # erics 123456
    if users.get(user_name)[0] == pwd:
        return generate_token(user_name)
    return '用户登录失败！'


@app.route('/test', methods=['GET'])
def test():
    """
    用于请求数据测试
    :return:
    """
    token = request.args.get('token')
    print(token, type(token))  # ZXJpY3M6MC40NzI1OTkwNTMzNjA3NDgyNjoxNTk2MTI3MjE5LjczMDU0OTM= <class 'str'>
    if verify_token(token) == 1:
        return '验证成功！'
    else:
        return '验证失败！'


#################### 授权服务器的编写 ##########################
def gen_auth_code(uri):
    code = random.randint(0, 10000)
    auth_code[code] = uri
    return code


@app.route('/client/login', methods=['GET', 'POST'])
def client_login():
    """
    步骤A：用户访问客户端的/login路径，客户端将用户重定向到授权服务器的/oauth路径并附上客户端代码以及重定向的uri(redirect_uri)
    :return:
    """
    uri = 'http://127.0.0.1:5000/oauth?response_type=code&client_name=%s&redirect_uri=%s' % (client_name, redirect_uri)
    return redirect(uri)


@app.route('/oauth', methods=['GET', 'POST'])
def oauth():
    if request.args.get('redirect_uri'):
        # 认证服务器把请求的uri保存起来
        oauth_redirect_uri.append(request.args.get('redirect_uri'))  # redirect_uri：http://127.0.0.1:5000/client/passport
    if request.args.get('user'):
        """
        步骤B：授权服务器要求用户给予授权，用户通过输入用户名和密码的方式来提供授权。
        """

        if users.get(request.args.get('user'))[0] == request.args.get('pwd') and oauth_redirect_uri:
            """
            授权服务器获取用户授权之后，将用户重定向到客户端所提供的uri,并附上授权码
            """
            uri = oauth_redirect_uri[0] + '?code=%s' % gen_auth_code(oauth_redirect_uri[0])
            return redirect(uri)

    if request.args.get('code'):
        """
        步骤D：授权服务器验证授权码和重定向uri的正确性，验证成功将为客户端发放token
        """
        if auth_code.get(int(request.args.get('code'))) == request.args.get('redirect_uri'):
            return generate_token(request.args.get('client_name'))

    return 'Please login!'


@app.route('/client/passport', methods=['GET', 'POST'])
def client_passport():
    """
    步骤C：客户端使用授权码和重定向uri向授权服务器请求token
    :return:
    """
    code = request.args.get('code')
    uri = 'http://127.0.0.1:5000/oauth?grant_type=authorization_code&code=%s&redirect_uri=%s&client_name=%s' % (
        code, redirect_uri, client_name)
    return redirect(uri)


if __name__ == '__main__':
    app.run(debug=True)

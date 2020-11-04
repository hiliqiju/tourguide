# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/31
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
from flask import current_app
from tourguide.models import Users
from typing import Union
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature


def generate_token(id: int, expiration: int = 600) -> str:
    # 600s
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': id}).decode('utf-8')


def verify_token(token: str) -> Union[object, dict]:
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        msg = {
            'code': 1002,
            'msg': 'token过期'
        }
    except BadSignature:
        msg = {
            'code': 1003,
            'msg': '无效的token'
        }
    else:
        msg = Users.query.get(data['id'])
    return msg

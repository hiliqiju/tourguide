# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/11/1
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from flask import Blueprint
from tourguide.models import Users
from tourguide.token import generate_token

admin_login_bp = Blueprint('admin_login', __name__)
api = Api(admin_login_bp)

admin_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'register_data': fields.DateTime
}

resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'token': fields.String,
    'info': fields.Nested(admin_fields)
}


def get_post_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('username', type=str, location='form', required=True, help='username是必需的')
    parses.add_argument('password', type=str, location='form', required=True, help='password是必需的')
    return parses.parse_args()


class Login(Resource):
    def get(self):
        ...

    @marshal_with(resource_fields)
    def post(self):
        args = get_post_parses()
        username = args.get('username')
        password = args.get('password')
        user = Users.query.filter(Users.username == username).first()
        if not user:
            return {
                'code': 400,
                'msg': '该用户不存在'
            }
        elif not user.check_password(password):
            return {
                'code': 400,
                'msg': '密码错误'
            }
        elif user.permission != '1':
            return {
                'code': 400,
                'msg': '该管理员不存在'
            }
        else:
            token = generate_token(user.id)
            return {
                'code': 200,
                'msg': '登录成功',
                'token': token,
                'info': user
            }

    def put(self):
        ...

    def delete(self):
        ...


api.add_resource(Login, '/tourguide/v1/admin/login')

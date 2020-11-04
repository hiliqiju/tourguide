# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/11/1
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from tourguide.models import Users
from tourguide.token import generate_token

login_bp = Blueprint('login', __name__)
api = Api(login_bp)

user_fields = {
    'id': fields.String,
    'username': fields.String,
    'register_date': fields.DateTime
}
resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'token': fields.String,
    'info': fields.Nested(user_fields)
}


def get_post_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('username', type=str, required=True, help='用户名是必需的', location='form')
    parses.add_argument('password', type=str, required=True, help='密码是必需的', location='form')
    return parses.parse_args()


class Login(Resource):
    def get(self):
        ...

    @marshal_with(resource_fields)
    def post(self):
        args = get_post_parses()
        username = args.get('username')
        password = args.get('password')
        # 获取username用的的所有信息
        user = Users.query.filter(Users.username == username).first()

        if not user:
            return {
                'code': 400,
                'msg': '用户不存在'
            }
        elif not user.check_password(password):
            return {
                'code': 400,
                'msg': '密码不正确'
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


api.add_resource(Login, '/tourguide/v1/user/login')

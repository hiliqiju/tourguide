# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/11/1
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse, marshal_with
from tourguide.models import Users
from tourguide.extentions import db

register_bp = Blueprint('register', __name__)
api = Api(register_bp)


def get_post_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('username', type=str, required=True, help='username是必需的', location='form')
    parses.add_argument('password', type=str, required=True, help='password是必需的', location='form')
    parses.add_argument('confirm_pwd', type=str, required=True, help='confirm_pwd是必需的', location='form')
    return parses.parse_args()


class Register(Resource):
    def get(self):
        ...

    def post(self):
        args = get_post_parses()
        username = args.get('username')
        password = args.get('password')
        confirm_pwd = args.get('confirm_pwd')

        if Users.query.filter(Users.username == username).first():
            return jsonify({
                'code': 409,
                'msg': '用户名已存在'
            })
        elif password != confirm_pwd:
            return jsonify({
                'code': 400,
                'msg': '密码不一致!'
            })
        else:
            user = Users(username, password)
            user.set_password(password)
            db.session.add(user)
            return jsonify({
                'code': 201,
                'msg': '注册成功'
            })

    def put(self):
        ...

    def delete(self):
        ...


api.add_resource(Register, '/tourguide/v1/user/register')

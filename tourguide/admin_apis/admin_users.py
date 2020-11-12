# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/11/1
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from tourguide.token import verify_token
from flask import Blueprint, jsonify
from tourguide.models import Users

admin_users_bp = Blueprint('admin_users', __name__)
api = Api(admin_users_bp)

users_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'register_date': fields.DateTime
}

resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'info': fields.List(fields.Nested(users_fields))
}


def get_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return parses.parse_args()


def get_del_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    parses.add_argument('id', type=int, location='form', required=True, help='id是必须的')
    return parses.parse_args()


class AdminUsers(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = get_parses()
        token = args.get('token')
        # 验证token
        msg = verify_token(token)
        if type(msg) is dict:
            return msg
        else:
            users = Users.query.filter(Users.username != 'admin').all()
            return {
                'code': 200,
                'msg': '请求成功',
                'info': users
            }

    def post(self):
        ...

    def put(self):
        ...

    def delete(self):
        args = get_del_parses()
        token = args.get('token')
        id = args.get('id')
        # 验证token
        msg = verify_token(token)
        if type(msg) is dict:
            return jsonify(msg)

        res = Users.query.filter(Users.id == id).delete()
        if res != 0:
            return jsonify({
                'code': 204,
                'msg': '删除成功'
            })
        else:
            return jsonify({
                'code': 200,
                'msg': '已删除'
            })


api.add_resource(AdminUsers, '/tourguide/v1/admin/users')

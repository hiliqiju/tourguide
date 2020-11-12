# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/11/1
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
from flask import Blueprint
from flask_restful import Resource, Api, fields, marshal_with
from tourguide.models import Scenery

scenery_bp = Blueprint('scenery', __name__)
api = Api(scenery_bp)

ticket = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String,
    'price': fields.Float
}

scenery = {
    'id': fields.Integer,
    'name': fields.String,
    'img_name': fields.String,
    'site': fields.String,
    'grade': fields.String,
    'introduce': fields.String,
    'open_time': fields.String,
    'ticket': fields.List(fields.Nested(ticket))
}

resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'scenery': fields.List(fields.Nested(scenery))
}


class GetScenery(Resource):
    @marshal_with(resource_fields)
    def get(self):
        scenerys = Scenery.query.all()
        return {
            'code': 200,
            'msg': '请求成功',
            'scenery': scenerys
        }

    def post(self):
        ...

    def put(self):
        ...

    def delete(self):
        ...


api.add_resource(GetScenery, '/tourguide/v1/scenery')

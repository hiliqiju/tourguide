# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/11/1
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
from flask import Blueprint, send_from_directory, g
from flask_restful import Resource, Api, reqparse

get_imgs_bp = Blueprint('get_imgs', __name__)
api = Api(get_imgs_bp)


def get_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('img_name', type=str, location='args', required=True, help='img_name是必需的')
    return parses.parse_args()


class GetImgs(Resource):
    def get(self):
        args = get_parses()
        img_name = args.get('img_name')
        # <img src="http://127.0.0.1:5000/tourguide/v1/get/img?img_name=lemon.jpg">
        print('------------------', g.PATH)
        return send_from_directory(g.PATH, img_name)

    def post(self):
        ...

    def put(self):
        ...

    def delete(self):
        ...


api.add_resource(GetImgs, '/tourguide/v1/get/img')

# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/11/1
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
from tourguide.token import verify_token
from tourguide.models import Scenery
from tourguide.extentions import db
from flask_restful import Resource, Api, reqparse
from flask import Blueprint, jsonify, g
from werkzeug.datastructures import FileStorage
import os

admin_scenery_bp = Blueprint('admin_scenery', __name__)
api = Api(admin_scenery_bp)


def get_post_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    parses.add_argument('name', type=str, location='form', required=True, help='name是必须的')
    parses.add_argument('img', type=FileStorage, location='files', required=True, help='img是必须的')
    parses.add_argument('site', type=str, location='form', required=True, help='site是必须的')
    parses.add_argument('grade', type=str, location='form', required=True, help='grade是必须的')
    parses.add_argument('introduce', type=str, location='form', required=True, help='introduce是必须的')
    parses.add_argument('open_time', type=str, location='form', required=True, help='open_time是必须的')
    return parses.parse_args()


def get_put_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    parses.add_argument('id', type=int, location='form', required=True, help='id是必须的')
    parses.add_argument('name', type=str, location='form', required=True, help='name是必须的')
    # parses.add_argument('img', type=FileStorage, location='files')
    parses.add_argument('site', type=str, location='form', required=True, help='site是必须的')
    parses.add_argument('grade', type=str, location='form', required=True, help='grade是必须的')
    parses.add_argument('introduce', type=str, location='form', required=True, help='introduce是必须的')
    parses.add_argument('open_time', type=str, location='form', required=True, help='open_time是必须的')
    return parses.parse_args()


def get_del_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    parses.add_argument('id', type=int, location='form', required=True, help='id是必须的')
    return parses.parse_args()


class AdminScenery(Resource):
    def get(self):
        ...

    def post(self):
        args = get_post_parses()
        token = args.get('token')
        name = args.get('name')
        img = args.get('img')
        site = args.get('site')
        grade = args.get('grade')
        introduce = args.get('introduce')
        open_time = args.get('open_time')
        # 验证token
        msg = verify_token(token)
        if type(msg) is dict:
            return jsonify(msg)
        else:
            img_name = img.filename
            img.save(os.path.join(g.PATH, img_name))
            db.session.add(Scenery(name, img_name, site, grade, introduce, open_time))
            return jsonify({
                'code': 201,
                'msg': '添加成功'
            })

    def put(self):
        print('----------put')
        args = get_put_parses()
        token = args.get('token')
        # 得到风景id, 用于更新
        id = args.get('id')
        name = args.get('name')
        # img = args.get('img')
        site = args.get('site')
        grade = args.get('grade')
        introduce = args.get('introduce')
        open_time = args.get('open_time')
        # 验证token
        msg = verify_token(token)
        if type(msg) is dict:
            return jsonify(msg)

        # if img is not None:
        #     img_name = img.filename  # 得到img本地路径
        #     img.save(os.path.join(g.PATH, img.filename))  # 将img存储到本地
        #     res = Scenery.query.filter(Scenery.id == id).update({
        #         'name': name,
        #         'img_name': img_name,
        #         'site': site,
        #         'grade': grade,
        #         'introduce': introduce,
        #         'open_time': open_time
        #     })
        # else:
        #     res = Scenery.query.filter(Scenery.id == id).update({
        #         'name': name,
        #         'site': site,
        #         'grade': grade,
        #         'introduce': introduce,
        #         'open_time': open_time
        #     })
        res = Scenery.query.filter(Scenery.id == id).update({
            'name': name,
            'site': site,
            'grade': grade,
            'introduce': introduce,
            'open_time': open_time
        })
        if res != 0:
            return jsonify({
                'code': 200,
                'msg': '更新成功'
            })
        else:
            return jsonify({
                'code': 200,
                'msg': '已更新'
            })

    def delete(self):
        args = get_del_parses()
        token = args.get('token')
        # 得到景区id
        id = args.get('id')
        # 验证token
        msg = verify_token(token)
        if type(msg) is dict:
            return jsonify(msg)

        scenery = Scenery.query.filter(Scenery.id == id).first()
        img_name = scenery.img_name
        img_path = os.path.join(g.PATH, img_name)
        # 删除该景区图片
        if os.path.exists(img_path):
            os.remove(img_path)
        # 删除该景区所有数据
        db.session.delete(scenery)
        return jsonify({
            'code': 204,
            'msg': '删除成功'
        })


api.add_resource(AdminScenery, '/tourguide/v1/admin/scenerys')

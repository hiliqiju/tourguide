# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/11/1
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
from tourguide.token import verify_token
from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from tourguide.models import Ticket, Scenery
from tourguide.extentions import db

admin_ticket_bp = Blueprint('admin_ticket', __name__)
api = Api(admin_ticket_bp)

ticket_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String,
    'price': fields.Float,
    'scenery_id': fields.Integer,
    'scen_name': fields.String
}
resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(ticket_fields))
}

def get_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return parses.parse_args()

def get_post_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    parses.add_argument('name', type=str, location='form', required=True, help='name是必须得')
    parses.add_argument('type', type=str, location='form', required=True, help='type是必须得')
    parses.add_argument('price', type=float, location='form', required=True, help='price是必须得')
    parses.add_argument('scenery_id', type=int, location='form', required=True, help='scenery_id是必须得')
    return parses.parse_args()


def get_put_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('id', type=int, location='form', required=True, help='id是必须得')
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    parses.add_argument('name', type=str, location='form', required=True, help='name是必须得')
    parses.add_argument('type', type=str, location='form', required=True, help='type是必须得')
    parses.add_argument('price', type=float, location='form', required=True, help='price是必须得')
    parses.add_argument('scenery_id', type=int, location='form', required=True, help='scenery_id是必须得')
    return parses.parse_args()


def get_del_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('id', type=int, location='form', required=True, help='id是必须得')
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return parses.parse_args()


class AdminTicket(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = get_parses()
        token = args.get('token')
        # 验证token
        msg = verify_token(token)
        if type(msg) is dict:
            return msg
        else:
            tickets = Ticket.query.all()
            return {
                'code': 200,
                'msg': '请求成功',
                'data': tickets
            }


    def post(self):
        args = get_post_parses()
        token = args.get('token')
        name = args.get('name')
        ticket_type = args.get('type')
        price = args.get('price')
        scenery_id = args.get('scenery_id')
        scen_name = Scenery.query(Scenery.name).filter(Scenery.id==id).first()
        # 验证token
        msg = verify_token(token)
        if type(msg) is dict:
            return jsonify(msg)

        db.session.add(Ticket(name, ticket_type, price, scenery_id, scen_name))
        return jsonify({
            'code': 201,
            'msg': '添加成功'
        })

    def put(self):
        args = get_put_parses()
        token = args.get('token')
        id = args.get('id')
        name = args.get('name')
        ticket_type = args.get('type')
        price = args.get('price')
        scenery_id = args.get('scenery_id')
        # 验证token
        msg = verify_token(token)
        if type(msg) is dict:
            return jsonify(msg)

        res = Ticket.query.filter(Ticket.id == id).update({
            'name': name,
            'type': ticket_type,
            'price': price,
            'scenery_id': scenery_id
        })
        if res != 0:
            return jsonify({
                'code': 201,
                'msg': '更新成功'
            })
        else:
            return jsonify({
                'code': 201,
                'msg': '已更新'
            })

    def delete(self):
        args = get_del_parses()
        token = args.get('token')
        id = args.get('id')
        # 验证token
        msg = verify_token(token)
        if type(msg) is dict:
            return jsonify(msg)

        res = Ticket.query.filter(Ticket.id == id).delete()
        if res != 0:
            return jsonify({
                'code': 204,
                'msg': '删除成功'
            })
        else:
            return jsonify({
                'code': 204,
                'msg': '已更新'
            })


api.add_resource(AdminTicket, '/tourguide/v1/admin/tickets')

# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/11/1
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
from flask import Blueprint, jsonify

from tourguide.extentions import db
from tourguide.token import verify_token
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from tourguide.models import Ticket, UserTicket

ticket_bp = Blueprint('ticket', __name__)
api = Api(ticket_bp)

user_ticket = {
    'id': fields.Integer,
    'phone': fields.String,
    'id_card': fields.String,
    'number': fields.Integer
}

tickets = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String,
    'price': fields.Float,
}

resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'ticket_info': fields.List(fields.Nested(user_ticket)),
    'ticket': fields.List(fields.Nested(tickets))
}


def get_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return parses.parse_args()


def get_post_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    parses.add_argument('ticket_id', type=int, location=['form', 'args'], required=True, help='ticket_id是必须的')
    parses.add_argument('phone', type=str, location='form', required=True, help='phone是必须的')
    parses.add_argument('id_card', type=str, location='form', required=True, help='id_card是必须的')
    parses.add_argument('number', type=int, location='form', required=True, help='number是必须的')
    return parses.parse_args()


class UserTickets(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = get_parses()
        token = args.get('token')
        # 验证token
        msg = verify_token(token)
        if type(msg) is dict:
            return msg

        # 得到该用户已购买的门票id
        ticket_ids = []
        for temp in msg.user_tickets:
            ticket_ids.append(temp.ticket_id)
        print('---------------------------', ticket_ids)
        tickets = []
        for id in ticket_ids:
            tickets.append(Ticket.query.filter(Ticket.id == id).first())
        return {
            'code': 200,
            'msg': '请求成功',
            'ticket_info': msg.user_tickets,
            'ticket': tickets
        }

    def post(self):
        args = get_post_parses()
        token = args.get('token')
        phone = args.get('phone')
        id_card = args.get('id_card')
        number = args.get('number')
        ticket_id = args.get('ticket_id')
        # 验证token
        msg = verify_token(token)
        if type(msg) is dict:
            return jsonify(msg)
        # 验证是否存在该门票
        if not Ticket.query.filter(Ticket.id == ticket_id).first():
            return jsonify({
                'code': 400,
                'msg': '该门票不存在'
            })
        else:
            db.session.add(UserTicket(phone, id_card, number, ticket_id, msg.id))
            return jsonify({
                'code': 200,
                'msg': '购票成功'
            })

    def put(self):
        ...

    def delete(self):
        ...


api.add_resource(UserTickets, '/tourguide/v1/user/ticket')

# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/31
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
from tourguide.extentions import db, bcrypt
from datetime import datetime
from typing import NoReturn


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名')
    password = db.Column(db.String(100), nullable=False, comment='用户密码')
    permission = db.Column(db.Enum('0', '1'), nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.now, comment='注册时间')
    user_tickets = db.relationship(
        'UserTicket',
        backref='users',
        lazy='dynamic',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def __init__(self, name: str, pwd: str, permission: str = '0') -> NoReturn:
        self.username = name
        self.password = pwd
        self.permission = permission

    def set_password(self, pwd: str = '123456') -> NoReturn:
        self.password = bcrypt.generate_password_hash(pwd)

    def check_password(self, pwd: str = '123456') -> str:
        return bcrypt.check_password_hash(self.password, pwd)


class Scenery(db.Model):
    __tablename__ = 'scenery'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False, comment='景区名称')
    img_name = db.Column(db.String(50), comment='景区图片名称')
    site = db.Column(db.String(100), nullable=False, comment='景区位置')
    grade = db.Column(db.String(20), nullable=False, comment='景区等级(AAAAA)')
    introduce = db.Column(db.Text, nullable=False, comment='景区介绍')
    open_time = db.Column(db.String(20), nullable=False, comment='开放时间')
    ticket = db.relationship(
        'Ticket',
        backref='scenery',
        lazy='dynamic',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def __init__(self, name: str, img_name: str, site: str, grade: str, introduce: str, open_time: str) -> NoReturn:
        self.name = name
        self.img_name = img_name
        self.site = site
        self.grade = grade
        self.introduce = introduce
        self.open_time = open_time


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False, comment='门票名称')
    type = db.Column(db.Enum('成人票', '儿童票'), nullable=False, comment='门票类型')
    price = db.Column(db.Float, nullable=False, comment='票价')
    user_tickets = db.relationship(
        'UserTicket',
        backref='ticket',
        lazy='dynamic',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    scenery_id = db.Column(db.Integer, db.ForeignKey('scenery.id', ondelete='CASCADE'))

    def __init__(self, name: str, type: str, price: float, scenery_id: int) -> NoReturn:
        self.name = name
        self.type = type
        self.price = price
        self.scenery_id = scenery_id


class UserTicket(db.Model):
    __tablename__ = 'userticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), nullable=False, comment='电话号码')
    id_card = db.Column(db.String(20), nullable=False, comment='身份证号')
    number = db.Column(db.Integer, nullable=False, comment='购买数量')
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __init__(self, phone: str, id_card: str, number: int, ticket_id: int, user_id: int) -> NoReturn:
        self.phone = phone
        self.id_card = id_card
        self.number = number
        self.ticket_id = ticket_id
        self.user_id = user_id

    def set_IDcard(self, id_card: str) -> NoReturn:
        self.id_card = bcrypt.generate_password_hash(id_card)

    def check_IDcard(self, id_card: str) -> str:
        return bcrypt.check_password_hash(self.id_card, id_card)

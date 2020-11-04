# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/31
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
import os
from flask import Flask, jsonify, g
from tourguide.models import Users, UserTicket, Scenery, Ticket
from tourguide.commands import register_commands
from tourguide.settings import config
from tourguide.extentions import db, bcrypt, migrate, cors
from tourguide.common_apis.get_imgs import get_imgs_bp
from tourguide.common_apis.get_scenery import scenery_bp
from tourguide.user_apis.login import login_bp
from tourguide.user_apis.register import register_bp
from tourguide.user_apis.user_ticket import ticket_bp
from tourguide.admin_apis.admin_login import admin_login_bp
from tourguide.admin_apis.admin_scenerys import admin_scenery_bp
from tourguide.admin_apis.admin_users import admin_users_bp
from tourguide.admin_apis.admin_tickets import admin_ticket_bp


def create_app(configName=None):
    if configName is None:
        configName = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    # 导入配置
    app.config.from_object(config[configName])
    # 注册扩展
    register_extentions(app)
    # 注册全局变量
    register_g(app)
    # 注册蓝图api
    register_apis(app)
    # 注册自定义命令
    register_commands(app)
    # 注册错误
    register_errors(app)

    return app


def register_extentions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/tourguide/v1/*": {"origins": "*"}})


def register_apis(app):
    app.register_blueprint(get_imgs_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(scenery_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(admin_login_bp)
    app.register_blueprint(admin_scenery_bp)
    app.register_blueprint(admin_users_bp)
    app.register_blueprint(admin_ticket_bp)


def register_g(app):
    @app.before_request
    def before_request():
        # 只能'static/imgs'
        g.PATH = os.path.join(app.root_path, 'static/imgs')


def register_errors(app):
    @app.errorhandler(404)
    def api_not_found(e):
        return jsonify({
            'code': 404,
            'msg': '未发现此接口'
        })

    @app.errorhandler(500)
    def interal_server_error(e):
        return jsonify({
            'code': 500,
            'msg': '服务器错误'
        })

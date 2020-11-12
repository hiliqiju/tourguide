# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/11/1
    @Gitee: https://gitee.com/missliqiju/tourguide.git
"""
import click
from tourguide.models import Users, UserTicket, Scenery, Ticket
from tourguide.extentions import db


def register_commands(app):
    @app.cli.command('init_data')
    def init_data():
        """初始化表数据"""
        click.echo('initializing the table data...')
        # 初始化users表
        user1 = Users('a', '123456')
        user2 = Users('b', '123456')
        user3 = Users('c', '123456')
        admin = Users('admin', '123456', '1')
        for u in [user1, user2, user3, admin]:
            u.set_password('123456')
        db.session.add_all([user1, user2, user3, admin])

        # 初始化scenery表
        s1 = Scenery('鼓浪屿风景区', 'gulangyu.jpg', '厦门市思明区鼓浪屿', '5A',
                     '''鼓浪屿是一个宁静美丽的小岛，凭借其独特的景色，已然成为厦门名副其实的旅游名片。岛上有日光岩、菽庄花园、风琴博物馆等景点，
                     在日光岩内，可以俯视全岛，将景色尽收眼底。除此之外，鼓浪屿上还有闽南建筑风格的海天堂构、中完合壁的八卦楼以及19世纪欧陆风格的
                     国家领事馆，因为这些多种风格的建筑，所以又有万国建筑博览之称。鼓浪屿有许多小资的店铺，装修的很文艺范儿，非常适合拍照。''', '全年全天开放')
        s2 = Scenery('西湖风景区', 'xihu.jpg', '杭州市西湖风景名胜区', '5A', '''西湖无疑是杭州之美的代表，很有名的“西湖十景”环绕湖边，自然与人文相互映衬，
        组成了杭州旅行的核心地带。你不必执着于走遍每个景点，倒可以花上半天或一天在湖边徜徉一番，无论怎么玩，都让人心情舒畅。''',
                     '全年全天开放')
        db.session.add_all([s1, s2])

        # 初始化Ticket表
        t1 = Ticket('日光岩', '成人票', 50.0, 1, '鼓浪屿风景区')
        t2 = Ticket('菽庄花园', '成人票', 30.0, 1, '鼓浪屿风景区')
        t3 = Ticket('皓月园', '成人票', 10.0, 1, '鼓浪屿风景区')
        t4 = Ticket('风琴博物馆', '成人票', 15.0, 1, '鼓浪屿风景区')
        t5 = Ticket('厦门海底世界', '成人票', 107.0, 1, '鼓浪屿风景区')
        t6 = Ticket('厦门海底世界', '儿童票', 58.0, 1, '鼓浪屿风景区')
        t7 = Ticket('灵隐飞来峰', '成人票', 45.0, 2, '西湖风景区')
        t8 = Ticket('灵隐飞来峰', '儿童票', 22.5, 2, '西湖风景区')
        t9 = Ticket('岳王庙', '成人票', 25.0, 2, '西湖风景区')
        t10 = Ticket('岳王庙', '儿童票', 12.5, 2, '西湖风景区')
        t11 = Ticket('北高峰索道', '成人票', 30.0, 2, '西湖风景区')
        db.session.add_all([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11])

        # 初始化userTicket表
        ut1 = UserTicket('17326400593', '2154314214324532', 1, 1, 1)
        ut2 = UserTicket('17626400124', '2135434214324532', 1, 1, 2)
        ut3 = UserTicket('16526400143', '4234314214324532', 2, 2, 1)
        ut4 = UserTicket('12326234593', '6554314214324532', 1, 2, 3)
        ut5 = UserTicket('16526403293', '3454314214324532', 2, 1, 2)
        db.session.add_all([ut1, ut2, ut3, ut4, ut5])

        click.echo('initializing data success.')

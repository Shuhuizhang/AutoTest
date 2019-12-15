# -*- coding:utf-8 -*-
# author: Steven
# datetime:2019/12/7 20:24
# software: PyCharm
# Description：用户相关api
import re

from flask import request, jsonify, current_app, session, g
from sqlalchemy.exc import IntegrityError

from managetest import db
from managetest.api_list import api
from managetest.models import User
from utils.commons import login_required


@api.route('/index', methods=["GET"])
@login_required
def index():
    """首页"""

    return jsonify(code=200, msg='欢迎进入Haizol AutoManage', user_name=g.user_name)


@api.route('/login', methods=["POST"])
def login():
    req_dict = request.get_json()
    email = req_dict.get("email")
    password = req_dict.get("password")

    # 校验参数
    # 参数完整的校验
    if not all([email, password]):
        return jsonify(code=402, message="参数不完整")

    # 邮箱的格式
    if not re.match(r"^([a-z]|[A-Za-z0-9]|[-]|[_][.])([A-Za-z0-9])+@([A-Za-z0-9]|[-])+\..+$", email):
        return jsonify(code=402, message="邮箱格式错误")

        # 从数据库中根据邮箱查询用户的数据对象
    try:
        user = User.query.filter_by(email=email).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=405, message="获取用户信息失败")
    if user.is_del == '1':
        return jsonify(code=402, message="用户账号已失效")

    if user is None or not user.check_password(password):
        # 如果验证失败，记录错误次数，返回信息
        return jsonify(code=402, message="用户名或密码错误")

    session["name"] = user.name
    session["email"] = user.email
    session["user_id"] = user.id

    return jsonify(code=200, message="登录成功")


@api.route('/register', methods=['POST'])
def register():
    req_dict = request.get_json()
    name = req_dict.get("name")
    email = req_dict.get("email")
    password = req_dict.get("password")

    if not all([email, password, name]):
        return jsonify(code=402, message="参数不完整")

    # 邮箱的格式
    if not re.match(r"^([a-z]|[A-Za-z0-9]|[-]|[_][.])([A-Za-z0-9])+@([A-Za-z0-9]|[-])+\..+$", email):
        return jsonify(code=402, message="邮箱格式错误")

    user = User(name=name, email=email)
    user.password = password

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        # 表示手机号出现了重复值，即手机号已注册过
        current_app.logger.error(e)
        return jsonify(code=402, message="邮箱已存在")
    except Exception as e:
        db.session.rollback()
        # 表示手机号出现了重复值，即手机号已注册过
        current_app.logger.error(e)
        return jsonify(code=405, message="查询数据库异常")

    return jsonify(code=200, message="新增用户成功")


@api.route("/check_login", methods=["GET"])
def check_login():
    """检查登陆状态"""
    # 尝试从session中获取用户的名字
    email = session.get("email")
    name = session.get("name")
    # 如果session中数据name名字存在，则表示用户已登录，否则未登录
    if email is not None:
        return jsonify(code=200, message="用户已登录", data={"name": name, 'email': email})
    else:
        return jsonify(code=403, message="用户未登录")


@api.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    return jsonify(code=403, message="用户已退出")


@api.route("/user", methods=["GET"])
@login_required
def user():
    users = User.query.all()
    user_li = []
    for u in users:
        user_li.append(u.to_dict())
    return jsonify(code=200, message="请求成功", data=user_li)


@api.route("/update_status", methods=["PUT"])
@login_required
def update_user_status():
    req_dict = request.get_json()
    status = req_dict.get("status")
    user_id = req_dict.get("user_id")
    if not all([user_id]):
        return jsonify(code=402, message="参数不完整")

    user = User.query.filter_by(id=user_id).first()
    if user:
        user.is_del = '0' if status else '1'

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=405, message="数据操作异常")
    return jsonify(code=200, message="更新成功")
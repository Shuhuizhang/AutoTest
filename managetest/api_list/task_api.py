# -*- coding:utf-8 -*-
# author: Steven
# datetime:2019/12/15 17:54
# software: PyCharm
# Description：测试任务
from flask import jsonify, current_app

from managetest.api_list import api
from managetest.models import TestPlan
from utils.commons import login_required


@api.route("/task_list", methods=['GET'])
@login_required
def task_list():
    try:
        plan_li = TestPlan.query.filter_by(is_del='0')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=9002, message="查询异常")
    task_li = []
    for i in plan_li:
        task_li.append(i.to_basic_dict())
    return jsonify(code=200, message="请求成功", data=task_li)




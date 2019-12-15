# -*- coding:utf-8 -*-
# author: Steven
# datetime:2019/12/7 19:55
# software: PyCharm
# Description：

from flask import Blueprint


# 创建蓝图对象
api = Blueprint("api_list", __name__)


from managetest.api_list import user_api, case_api, task_api



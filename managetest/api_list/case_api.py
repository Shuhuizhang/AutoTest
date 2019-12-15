# -*- coding:utf-8 -*-
# author: Steven
# datetime:2019/12/11 22:31
# software: PyCharm
# Description：用例相关接口
from flask import request, jsonify, current_app

from managetest import db
from managetest.api_list import api
from managetest.models import TestCase
from utils.commons import login_required
from sqlalchemy import or_, desc


@api.route("/case_list", methods=['GET'])
@login_required
def case_list():
    """查询用例列表"""
    keyword = request.args.get('keyword')
    pagenum = request.args.get('pagenum')
    pagesize = request.args.get('pagesize')
    case_li = []
    try:
        pagenum = int(pagenum)
        pagesize = int(pagesize)
    except Exception as e:
        current_app.logger.error(e)
        pagenum = 1
        pagesize = 15
    if keyword and not keyword == '':
        test_cases = TestCase.query.filter_by(is_del='0').filter(or_(TestCase.clazz.like("%" + keyword + "%"),
                                                                     TestCase.module.like("%" + keyword + "%"),
                                                                     TestCase.method.like("%" + keyword + "%"),
                                                                     TestCase.remark.like("%" + keyword + "%"),
                                                                     )).order_by(desc('id'))
    else:
        test_cases = TestCase.query.filter_by(is_del='0').order_by(desc('id'))
        # 处理分页
    try:
        #                               当前页数          每页数据量                              自动的错误输出
        page_obj = test_cases.paginate(page=pagenum, per_page=pagesize, error_out=False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=9002, message="查询异常")

    cases = page_obj.items
    total = page_obj.total

    for case in cases:
        case_li.append(case.to_basic_dict())

    return jsonify(code=200, message='查询成功', data={'total': total, 'case_li': case_li, "current_page": pagenum})


@api.route("/saveCase", methods=['POST'])
@login_required
def saveCase():
    req_dict = request.get_json()
    id = req_dict.get('id')
    module = req_dict.get('module')
    clazz = req_dict.get('clazz')
    method = req_dict.get('method')
    remark = req_dict.get('remark')
    remark = remark if remark else ''

    if not all([module, clazz, method]):
        return jsonify(code=402, message="参数不完整")

    if not id:
        case = TestCase(module=module, clazz=clazz, method=method, remark=remark)
        try:
            db.session.add(case)
            db.session.commit()
            return jsonify(code=200, message="新增成功")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=405, message="数据库新增数据异常")
    else:
        case = TestCase.query.get(id)
        case.module = module
        case.clazz = clazz
        case.method = method
        case.remark = remark
        try:
            db.session.commit()
            return jsonify(code=200, message="修改成功")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=405, message="数据库操作数据异常")


@api.route("/get_case_by_id")
@login_required
def get_case():
    try:
        id = int(request.args.get('id'))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=420, message="请求参数错误")
    try:
        test_case = TestCase.query.get(id)
        return jsonify(code=200, message='查询成功', data=test_case.to_basic_dict())
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=9002, message="查询异常")


@api.route("/delete_case", methods=['DELETE'])
@login_required
def delete():
    try:
        id = int(request.args.get('id'))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=420, message="请求参数错误")
    try:
        test_case = TestCase.query.get(id)
        test_case.is_del = '1'
        db.session.commit()
        return jsonify(code=200, message='删除成功')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=9002, message="数据异常")


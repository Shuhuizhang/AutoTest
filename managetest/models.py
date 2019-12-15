# -*- coding:utf-8 -*-
# author: Steven
# datetime:2019/12/8 10:59
# software: PyCharm
# Description：定义模型
from datetime import datetime

from sqlalchemy import desc

from managetest import db
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel:
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间
    is_del = db.Column(db.String(2), default='0', nullable=False)


class User(BaseModel, db.Model):
    """用户"""

    __tablename__ = "tb_user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    name = db.Column(db.String(32), nullable=False)  # 用户暱称
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码

    # 加上property装饰器后，会把函数变为属性，属性名即为函数名
    @property
    def password(self):
        """读取属性的函数行为"""
        # print(user.password)  # 读取属性时被调用
        # 函数的返回值会作为属性值
        # return "xxxx"
        raise AttributeError("这个属性只能设置，不能读取")

    # 使用这个装饰器, 对应设置属性操作
    @password.setter
    def password(self, value):
        """
        设置属性  user.passord = "xxxxx"
        :param value: 设置属性时的数据 value就是"xxxxx", 原始的明文密码
        :return:
        """
        self.password_hash = generate_password_hash(value)

    def check_password(self, passwd):
        """
        检验密码的正确性
        :param passwd:  用户登录时填写的原始密码
        :return: 如果正确，返回True， 否则返回False
        """
        return check_password_hash(self.password_hash, passwd)

    def to_dict(self):
        """将对象转换为字典数据"""
        user_dict = {
            "user_id": self.id,
            "name": self.name,
            "email": self.email,
            "status": True if self.is_del == '0' else False,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return user_dict


class TestCase(BaseModel, db.Model):
    """测试用例"""
    __tablename__ = "tb_test_case"

    id = db.Column(db.Integer, primary_key=True)  # 用列编号
    module = db.Column(db.String(128), nullable=False)  # 用例模块
    clazz = db.Column(db.String(128), nullable=False)  # 用例所属类
    method = db.Column(db.String(128), nullable=False)  # 用例方法
    remark = db.Column(db.String(225))  # 用例描述

    def to_basic_dict(self):
        """将基本信息转换为字典数据"""
        case_dict = {
            "id": self.id,
            "module": self.module,
            "clazz": self.clazz,
            "method": self.method,
            "remark": self.remark,
        }
        return case_dict


class TestPlan(BaseModel, db.Model):
    """测试任务"""
    __tablename__ = "tb_test_plan"

    id = db.Column(db.Integer, primary_key=True)  # 任务id
    name = db.Column(db.String(128), nullable=False)  # 任务名称
    remark = db.Column(db.String(225))  # 任务描述
    task = db.Column(db.String(128))  # 定时执行时间
    status = db.Column(db.String(1), nullable=False, default='0')
    reports = db.relationship('TestReport', backref='TestPlan')

    def to_basic_dict(self):
        """将基本信息转换为字典数据"""
        task_dict = {
            "id": self.id,
            "name": self.name,
            "remark": self.remark if self.remark else '',
            "task": self.task if self.task else '',
            "report": self.reports[-1].name if not len(self.reports) == 0 else '',
            "status": self.status
        }
        return task_dict


class TestVersion(BaseModel, db.Model):
    """测试版本"""
    __tablename__ = "tb_test_version"

    id = db.Column(db.Integer, primary_key=True)  # 版本id
    name = db.Column(db.String(128), nullable=False)  # 版本名称
    remark = db.Column(db.String(225))  # 描述


class TestReport(BaseModel, db.Model):
    """测试报告"""
    __tablename__ = "tb_test_report"

    id = db.Column(db.Integer, primary_key=True)  # 报告id
    name = db.Column(db.String(225), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('tb_test_plan.id'))  # 所属的测试任务
    version = db.Column(db.Integer, db.ForeignKey('tb_test_version.id'))  # 测试版本



case_plan = db.table(
    'tb_case_plan',
    db.Column("case_id", db.Integer, db.ForeignKey("tb_test_case.id"), primary_key=True),  # 房屋编号
    db.Column("plan_id", db.Integer, db.ForeignKey("ih_facility_info.id"), primary_key=True)  # 设施编号
)


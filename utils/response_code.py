# coding:utf-8

class CODE:
    OK                  = "200"
    DBERR               = "4001"
    NODATA              = "4002"
    DATAEXIST           = "4003"
    DATAERR             = "4004"
    SESSIONERR          = "401"
    LOGINERR            = "4102"
    PARAMERR            = "420"
    USERERR             = "4104"
    ROLEERR             = "4105"
    PWDERR              = "4106"
    REQERR              = "4201"
    IPERR               = "4202"
    THIRDERR            = "4301"
    IOERR               = "4302"
    SERVERERR           = "4500"
    UNKOWNERR           = "4501"

message_map = {
    CODE.OK                    : u"请求成功",
    CODE.DBERR                 : u"数据库查询错误",
    CODE.NODATA                : u"无数据",
    CODE.DATAEXIST             : u"数据已存在",
    CODE.DATAERR               : u"数据错误",
    CODE.SESSIONERR            : u"用户未登录",
    CODE.LOGINERR              : u"用户登录失败",
    CODE.PARAMERR              : u"参数错误",
    CODE.USERERR               : u"用户不存在或未激活",
    CODE.ROLEERR               : u"用户身份错误",
    CODE.PWDERR                : u"密码错误",
    CODE.REQERR                : u"非法请求或请求次数受限",
    CODE.IPERR                 : u"IP受限",
    CODE.THIRDERR              : u"第三方系统错误",
    CODE.IOERR                 : u"文件读写错误",
    CODE.SERVERERR             : u"内部错误",
    CODE.UNKOWNERR             : u"未知错误",
}

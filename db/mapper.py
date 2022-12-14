from .postgesql import dao as pgDao
from .firebird import dao as fbDao


def getUserInfo(user_id):
    return pgDao.getUserInfo(user_id)


def getToken(user_id):
    return pgDao.getToken(user_id)


def updateToken(user_id, token):
    return pgDao.updateToken(user_id, token)


def getCounteragentByMod(branch_id):
    res, fld = fbDao.getCounteragentInfo(branch_id)
    return res, fld


def CLOSE_MDLP():
    fbDao.CLOSE()

import psycopg2
from .model import *


def getDatabaseMetadata(alias: str):
    data = PgDatabaseMetadata()
    if alias == 'mdlp':
        data.alias = alias
        data.host = 'localhost'
        data.port = 5432
        data.user = 'postgres'
        data.password = 'D5314384F'

    return data


def getCursor(alias):
    dbInfo = getDatabaseMetadata(alias)
    con = psycopg2.connect(database=dbInfo.alias, user=dbInfo.user, password=dbInfo.password, host=dbInfo.host, port=dbInfo.port)
    cur = con.cursor()
    return cur

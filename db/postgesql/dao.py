from .core import *


def getUserInfo(user_id):
    cur = getCursor('mdlp')
    cur.execute(f"""
        select s.client_id,
               s.client_secret,
               u.user_id as user_id,
               u.thumbprint_public_cert as thumbprint
        from sys.user_data u
            left join sys.account_system s on s.sys_id = u.sys_id
        where u.user_id = '{user_id}' :: uuid;
    """)
    res = cur.fetchone()
    cur.close()
    cur.connection.close()
    return res


def getToken(user_id):
    cur = getCursor('mdlp')
    cur.execute(f"select token, token_date from sys.user_data where user_id = '{user_id}' :: uuid;")
    res = cur.fetchone()
    cur.close()
    cur.connection.close()
    return res


def updateToken(user_id, token):
    cur = getCursor('mdlp')
    cur.execute(f"update sys.user_data set token = '{token}', token_date = now() where user_id = '{user_id}' :: uuid;")
    cur.connection.commit()
    cur.close()
    cur.connection.close()

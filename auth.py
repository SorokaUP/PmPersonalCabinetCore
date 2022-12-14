import os
import clr
# region CryptApi
this_dir = os.path.dirname(os.path.realpath(__file__))
clr.AddReference(this_dir + "\\CryptApi.dll")  # Mdlp.sln -> CryptApi => CryptApi.dll -> WinApiCrypt -> SignToBase64
from CryptApi import WinApiCrypt
# endregion
import json
from core import *


def sys_get_code(user: dict[str: str]) -> str:
    url = apiEndpoint + apiVersion + "auth"

    win_http = request_post_new_instance(url)
    win_http.SetRequestHeader("Content-Type", appjsutf8)
    win_http.Send(json.dumps(user))
    # print(win_http.ResponseText)
    return json.loads(win_http.ResponseText)['code']


def sys_get_signature(fingerprint: str, code: str) -> str:
    # Вызов .dll основанной на C# из боевого проекта
    # Mdlp.sln -> CryptApi => CryptApi.dll -> WinApiCrypt -> SignToBase64
    x = WinApiCrypt()
    sign = x.SignToBase64(bytes(code, 'utf-8'), fingerprint)
    return sign


def sys_get_token(code: str, thumbprint: str) -> str:
    url = apiEndpoint + apiVersion + "token"
    signature = sys_get_signature(thumbprint, code)
    data = {
        'code': code,
        'signature': signature
    }

    win_http = request_post_new_instance(url)
    win_http.SetRequestHeader("Content-Type", appjsutf8)
    win_http.Send(json.dumps(data))
    # print(win_http.ResponseText)
    token = json.loads(win_http.ResponseText)['token']
    return token


def auth(user_id: str, user_data: dict[str: str], thumbprint: str) -> str:
    print('Авторизуюсь (%s): Код...' % user_id, end=' ')
    code = sys_get_code(user_data)
    print('Токен...', end=' ')
    token = sys_get_token(code, thumbprint)
    print('Успешно.')
    return token

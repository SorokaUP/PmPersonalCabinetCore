import win32com.client

apiHost = 'api.mdlp.crpt.ru'
apiEndpoint = 'https://%s/' % apiHost
apiVersion = 'api/v1/'
apiUrl = apiEndpoint + apiVersion

appjs = 'application/json'
appjsutf8 = 'application/json;charset=UTF-8'


def request_post_new_instance(url: str):
    win_http = win32com.client.Dispatch('WinHTTP.WinHTTPRequest.5.1')
    # win_http.SetAutoLogonPolicy(0) #Автовход в систему
    win_http.Open("POST", url, False)
    return win_http


def request_get_new_instance(url: str):
    win_http = win32com.client.Dispatch('WinHTTP.WinHTTPRequest.5.1')
    # win_http.SetAutoLogonPolicy(0) #Автовход в систему
    win_http.Open("GET", url, False)
    return win_http


def request_fill_header(win_http, token: str):
    win_http.SetRequestHeader("Accept", appjsutf8)
    win_http.SetRequestHeader("Content-Type", appjsutf8)
    win_http.SetRequestHeader("Authorization", "token %s" % token)

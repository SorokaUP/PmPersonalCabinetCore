from core import *
import json
from timeout import method_timeout


def timeout(url: str):
    if url in method_timeout:
        method_timeout[url].timeout()
    else:
        method_timeout['default'].timeout()


def master_post(token: str, url: str, body) -> json:
    win_http = request_post_new_instance(apiUrl + url)
    request_fill_header(win_http, token)
    timeout(url)
    win_http.Send(json.dumps(body))
    # print(win_http.ResponseText)  # Может придти в битой кодировке windows-1251
    data = json.loads(win_http.ResponseText)
    return data


def master_get(token: str, url: str, *args: str) -> json:
    def extract_block(s: str) -> str:
        a = s.find('{')
        b = s.find('}')
        if a < 0 or b < 0:
            return ''
        return s[a: b + 1]

    # prepare url -> replace {...} to arg
    for arg in args:
        ext_block = extract_block(url)
        if ext_block != '':
            url = url.replace(ext_block, arg)

    win_http = request_get_new_instance(apiUrl + url)
    request_fill_header(win_http, token)
    timeout(url)
    win_http.Send()
    print(win_http.ResponseText)

    data = json.loads(win_http.ResponseText)
    return data


############################################################################################################
# implementation https://mdlp.crpt.ru/static/document/api_mdlp_ru.pdf
# Сорокин В.С. от 30.06.2022


# region ДОКУМЕНТЫ


# 5.1. Отправка документа
def send_doc(token):
    url = "documents/send"
    data = master_post(token, url, '')
    raise NotImplemented


# 5.2. Отправка документа большого объема
def send_large_doc(token):
    url = "documents/send_large"
    data = master_post(token, url, '')
    raise NotImplemented


# 5.11. Получение списка исходящих документов
def get_outcome_doc(token):
    url = "documents/outcome"
    data = master_post(token, url, '')
    raise NotImplemented


# 5.13. Получение списка входящих документов
def get_income_doc(token):
    url = "documents/income"
    data = master_post(token, url, '')
    raise NotImplemented


# 5.16. Получение метаданных документа
def get_metadata_doc(token, doc_id):
    url = f"documents/{doc_id}"
    data = master_get(token, url)
    raise NotImplemented


# 5.17. Получение документа по идентификатору
def get_doc_by_id(token, doc_id):
    url = f"documents/download/{doc_id}"
    data = master_get(token, url)
    raise NotImplemented


# 5.18. Получение списка документов по идентификатору запроса
def get_doc_by_request_id(token, request_id):
    url = f"documents/request/{request_id}"
    data = master_get(token, url)
    raise NotImplemented


# 5.19. Получение квитанции по номеру исходящего документа
def get_ticket_doc(token, doc_id):
    url = f"documents/{doc_id}/ticket"
    data = master_get(token, url)
    raise NotImplemented


# endregion
# region МОД / МОХ


# 8.1.2. Метод для поиска информации о местах осуществления деятельности по фильтру
def get_mod_info_filter(token):
    url = "reestr/branches/filter"
    data = master_post(token, url, '')
    raise NotImplemented


# 8.1.3. Получение перечня мест осуществления деятельности в системе
def get_mod_list(token):
    url = "reestr/branches/public/filter"
    data = master_post(token, url, '')
    raise NotImplemented


# 8.1.4. Получение информации о конкретном месте осуществления деятельности
def get_mod_info(token, branch_id):
    url = f"reestr/branches/{branch_id}"
    data = master_get(token, url)
    raise NotImplemented


# 8.2.2. Метод для поиска информации о местах ответственного хранения по фильтру
def get_moh_info_filter(token):
    url = "reestr/warehouses/filter"
    data = master_post(token, url, '')
    raise NotImplemented


# 8.2.3. Получение перечня мест ответственного хранения в системе
def get_moh_list(token):
    url = "reestr/warehouses/public/filter"
    data = master_post(token, url, '')
    raise NotImplemented


# 8.2.4. Получение информации о конкретном месте ответственного хранения
def get_moh_info(token, warehouse_id):
    url = f"reestr/warehouses/{warehouse_id}"
    data = master_get(token, url)
    raise NotImplemented


# endregion
# region КИЗ


# 8.3.1. Метод поиска по реестрам КИЗ
def get_kiz_info(token):
    url = "reestr/sgtin/filter"
    data = master_post(token, url, '')
    raise NotImplemented


# 8.3.2. Метод поиска по реестрам КИЗ по списку значений
def get_kiz_info_filter(token):
    url = "reestr/sgtin/sgtins-by-list"
    data = master_post(token, url, '')
    raise NotImplemented


# 8.3.3. Метод поиска по общедоступным реестрам КИЗ по списку значений
def get_kiz_info_public(token, sgtin):
    url = "reestr/sgtin/public/sgtins-by-list"
    body = {'filter': {'sgtins': sgtin}}

    data = master_post(token, url, body)
    return data


# 8.3.4. Метод поиска по общедоступному реестру КИЗ в архивном хранилище по списку значений
def get_kiz_info_public_archive(token):
    url = "reestr/sgtin/public/archive/sgtins-by-list"
    data = master_post(token, url, '')
    raise NotImplemented


# 8.3.5. Метод для получения из реестров КИЗ детальной информации о КИЗ и связанным с ним ЛП
def get_kiz_detail(token, sgtin):
    url = f"reestr/sgtin/{sgtin}"
    data = master_get(token, url)
    raise NotImplemented


# 8.3.6. Метод для получения детальной информации о КИЗ в архивном хранилище и связанным с ним ЛП
def get_kiz_detail_archive(token, sgtin):
    url = f"reestr/sgtin/archive/{sgtin}"
    data = master_get(token, url)
    raise NotImplemented


# 8.3.7. Метод для получения перечня документов по идентификатору КИЗ
def get_kiz_doc(token, sgtin):
    url = f"reestr/sgtin/documents?sgtin={sgtin}"
    data = master_get(token, url)
    raise NotImplemented


# 8.3.8. Метод для получения перечня документов по идентификатору КИЗ из архивного хранилища
def get_kiz_doc_archive(token, sgtin):
    url = f"reestr/sgtin/archive/documents?sgtin={sgtin}"
    data = master_get(token, url)
    raise NotImplemented


# endregion
# region DataMatrix


# 8.4.2. Метод валидации кода маркировки
def check_datamatrix(token):
    url = "sgtin/validate"
    data = master_post(token, url, '')
    raise NotImplemented


# 8.4.3. Метод верификации кода маркировки и криптохвоста
def check_verify_datamatrix(token):
    url = "sgtin/verification"
    data = master_post(token, url, '')
    raise NotImplemented


# endregion
# region SSCC


# 8.5.1. Метод для получения информации об иерархии вложенности третичной упаковки
def get_hierarchy_sscc(token, sscc):
    url = f"reestr/sscc/{sscc}/hierarchy"
    data = master_get(token, url)
    raise NotImplemented


# 8.5.2. Метод для получения информации о КИЗ в третичной упаковке
def get_kiz_info_sscc(token, sscc):
    url = f"reestr/sscc/{sscc}/sgtins"
    data = master_post(token, url, '')
    raise NotImplemented


# 8.5.3. Метод для получения информации о полной иерархии вложенности третичной упаковки
def get_full_hierarchy_sscc(token, sscc):
    url = f"reestr/sscc/{sscc}/full-hierarchy"
    data = master_get(token, url)
    raise NotImplemented


# 8.5.4. Метод для получения информации о полной иерархии вложенности третичной упаковки для нескольких SSCC
def get_full_hierarchy_many_sscc(token, *sscc_list):
    param: str = ''
    for sscc in sscc_list:
        if param != '':
            param.join('&')
        param.join(f'sscc={sscc}')

    url = f"reestr/sscc/full-hierarchy?{param}"
    data = master_get(token, url)
    raise NotImplemented


# 8.5.5. Метод для получения информации о существующем SSCC
def get_sscc_info(token, sscc_list):
    url = "reestr/sscc/sscc_check"
    body = {'sscc': sscc_list}

    data = master_post(token, url, body)
    return data


# endregion
# region КОНТРАГЕНТЫ


# 8.8.1. Метод добавления доверенного контрагента
def counteragent_add_verify(token):
    url = "reestr/trusted_partners/add"
    data = master_post(token, url, '')
    raise NotImplemented


# 8.8.2. Метод удаления доверенного контрагента
def counteragent_del_verify(token):
    url = "reestr/trusted_partners/delete"
    data = master_post(token, url, '')
    raise NotImplemented


# 8.8.3. Метод фильтрации доверенных контрагентов
def get_verify_counteragent(token):
    url = "reestr/trusted_partners/filter"
    data = master_post(token, url, '')
    raise NotImplemented


# endregion

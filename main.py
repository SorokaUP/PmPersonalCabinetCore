import config
import method
from model.Sgtin import Sgtin
from model.Sscc import Sscc
from model.Kiz import Kiz
from db import mapper as db
from model.UserInfo import UserInfo


def first_init():
    ui = db.getUserInfo(config.user_id)
    config.user_info = UserInfo(ui)


def api_search_kiz(kiz_list):
    def extract_kiz(kiz_type):
        def clear_kiz(item):
            return item\
                .replace('"', '')\
                .replace("'", '')\
                .replace(' ', '')\
                .replace('*', '')\
                .replace('•', '')\
                .replace('-', '')\
                .replace('+', '')\
                .replace('\n', '')

        lst = set()
        for item in kiz_list:
            kiz = clear_kiz(item)

            if kiz_type == 'sgtin':
                if len(kiz) == 27:
                    lst.add(kiz)
            else:
                if len(kiz) == 18:
                    lst.add(kiz)

        return lst

    def get(fun, lst):
        raw_data = None
        if len(lst) > 0:
            raw_data = fun(config.user_info.get_token(), list(lst))
            # print(raw_data)
        return raw_data

    def get_mod_list(raw_sgtin, raw_sscc):
        global raw_mod_list

        def extract_mod_list(lst):
            def extract_mod_json(item):
                if 'branch_id' in item:
                    return str(item['branch_id'])
                elif 'owner_id' in item:
                    return str(item['owner_id'])
                else:
                    return ''

            res = set()

            if lst is None:
                return res

            if 'entries' in lst:
                for item in lst['entries']:
                    mod = extract_mod_json(item)
                    if mod != '' and mod != 'None':
                        res.add(mod)

            return res

        def get_from_db():
            global raw, fld

            def x(f, d=''):
                if raw is None:
                    return ''
                if f in fld:
                    val = raw[fld.index(f)]
                    if val is None:
                        return d
                    return str(val)
                else:
                    return d

            res = []
            for mod in raw_mod_list:
                raw, fld = db.getCounteragentByMod(mod)
                res.append({
                    'NAME': x('NAME'),
                    'INN': x('INN'),
                    'SYS_ID': x('SYS_ID'),
                    'ADDRESS_NAME': x('ADDRESS_NAME'),
                    'ADDRESS_GUID': x('ADDRESS_GUID'),
                    'MOD': mod
                })

            db.CLOSE_MDLP()
            return res

        raw_mod_list_sgtin = extract_mod_list(raw_sgtin)
        raw_mod_list_sscc = extract_mod_list(raw_sscc)

        raw_mod_list = set()
        for mod in raw_mod_list_sgtin:
            raw_mod_list.add(mod)
        for mod in raw_mod_list_sscc:
            raw_mod_list.add(mod)

        res = get_from_db()
        return res

    def make_entries(raw_sgtin, raw_sscc, mod_list):
        def prepare(lst, kiz_type, mod_list):
            res = []

            if lst is None:
                return res

            kiz: Kiz
            for item in lst['entries']:
                kiz = Kiz()

                if kiz_type == 'sgtin':
                    sg = Sgtin(item)
                    kiz.fillSgtin(sg)
                else:
                    ss = Sscc(item)
                    kiz.fillSscc(ss)

                kiz.fillModFromList(mod_list)
                res.append(kiz.__dict__)

            return res

        res = []

        entries_sgtin = prepare(raw_sgtin, 'sgtin', mod_list)
        entries_sscc = prepare(raw_sscc, 'sscc', mod_list)

        for item in entries_sgtin:
            res.append(item)

        for item in entries_sscc:
            res.append(item)

        return res

    def make_failed(raw_sgtin, raw_sscc):
        def prepare(lst, kiz_type):
            res = []

            if lst is None:
                return res

            if 'failed_entries' not in lst:
                return res

            for item in lst['failed_entries']:
                res.append({
                    'kiz': str(item) if kiz_type == 'sgtin' else str(item['sscc']),
                    'error_code': '2' if kiz_type == 'sgtin' else str(item['error_code']),
                    'error_desc': 'Запрашиваемые данные не найдены' if kiz_type == 'sgtin' else str(item['error_desc'])
                })

            return res

        res = []

        failed_sgtin = prepare(raw_sgtin, 'sgtin')
        failed_sscc = prepare(raw_sscc, 'sscc')

        for item in failed_sgtin:
            res.append(item)

        for item in failed_sscc:
            res.append(item)

        return res

    # Инициализация пользователя
    first_init()

    # Распределяем коды на sgtin и sscc
    sgtin_list = extract_kiz('sgtin')
    sscc_list = extract_kiz('sscc')

    # Запрос данных из МДЛП
    raw_sgtin = get(method.get_kiz_info_public, sgtin_list)
    raw_sscc = get(method.get_sscc_info, sscc_list)

    # Отбираем информацию о местах деятельности
    mod_list = get_mod_list(raw_sgtin, raw_sscc)

    # Подготавливаем итоговые данные
    entries = make_entries(raw_sgtin, raw_sscc, mod_list)
    failed = make_failed(raw_sgtin, raw_sscc)

    res = {
        'entries': entries,
        'failed_entries': failed
    }
    return res


def main():
    data = api_search_kiz(["046071598604081W3ER00000000", "046071598604081W3ERPCKD3T0C", "0460715986040828SVYAM5YX3NY", "046400186411386528734054135", "046400186411383914344477297", "0475023200591002062UMF5L03R", "0475023200591002062UMG5NS2F", "042503695090651121352426121", "042503695090651121352436169", "0475023200591002060ANP4C2CC", "0475023200591002060ANR83ZTP", '059447282610915485', '589017830000023675', '146501092334774466', '146501092383403058'])
    print(data)
    pass


if __name__ == '__main__':
    main()

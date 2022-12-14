from . import Sgtin
from . import Sscc


status_kiz = {
    "in_circulation": "В обороте",
    "in_realization": "Отгружен",
    "transfer_to_agent": "Отгружен по агентскому договору",
    "change_owner_state_gov": "Ожидает подтверждения получения новым владельцем",
    "waiting_confirmation": "Ожидает подтверждения",
    "in_arbitration": "В арбитраже",
    "moved_for_disposal": "Передан на уничтожение",
    "disposed": "Уничтожен",
    "out_of_circulation": "Выведен из оборота",
    "experiment_outbound": "Выведен из оборота (накопленный в рамках эксперимента)",
    "in_sale": "Продан в розницу",
    "in_partial_sale": "Частично продан в розницу",
    "in_discount_prescription_sale": "Отпущен по льготному рецепту",
    "in_partial_discount_prescription_sale": "Частично отпущен по льготному рецепту",
    "in_medical_use": "Выдан для медицинского применения",
    "in_partial_medical_use": "Частично выдан для медицинского применения",
    "moved_to_unregistered": "Отгружен на незарегистрированное место деятельности",
    "moved_to_eeu": "Отгружен в ЕАЭС",
    "marked": "Ожидает выпуска",
    "lp_sampled": "Отобран образец",
    "transfered_to_owner": "Ожидает подтверждения получения собственником",
    "shipped": "Отгружен в РФ",
    "arrived": "Ввезен на территорию РФ",
    "declared": "Задекларирован",
    "paused_circulation": "Оборот приостановлен",
    "relabeled": "Перемаркирован",
    "reexported": "Реэкспорт",
    "released_contract": "Ожидает передачи собственнику",
    "released_foreign": "для типа эмиссии 3?—?Ожидает отгрузки в РФ || для типа эмиссии 4?—?Маркирован в ЗТК",
    "expired": "Срок годности истек",
    "change_owner": "Ожидает подтверждения смены собственника",
    "confirm_return_paused": "Ожидает подтверждения возврата приостановленных лекарственных препаратов",
    "moved_to_warehouse": "Принят на склад из ЗТК",
    "emission": "Эмитирован",
    "ofd_retail_error": "Продан в розницу с использованием ККТ с ошибкой",
    "ofd_discount_prescription_error": "Отпущен по льготному рецепту с использованием ККТ с ошибкой",
    "transferred_for_release": "Ожидает подтверждения получения собственником до ввода в оборот",
    "waiting_for_release": "Ожидает ввода в оборот собственником",
    "emitted": "Эмитирован",
    "marked_not_paid": "Ожидает выпуска, не оплачен",
    "released_foreign_not_paid": "для типа эмиссии 3?—?Ожидает отгрузки в РФ, не оплачен || для типа эмиссии 4?—?Маркирован в ЗТК, не оплачен",
    "expired_not_paid": "Истек срок ожидания оплаты",
    "emitted_paid": "Эмитирован, готов к использованию",
    "discount_prescription_error": "Отпущен по льготному рецепту с использованием РВ с ошибкой",
    "med_care_error": "Выдан для медицинского применения с использованием РВ с ошибкой",
    "declared_warehouse": "Принят на склад из ЗТК",
    "transferred_to_customs": "Передан для маркировки в ЗТК",
    "transferred_to_importer": "Ожидает подтверждения импортером",
    "transfer_to_production": "Ожидает подтверждения возврата",
    "waiting_change_property": "Ожидает подтверждения корректировки",
    "eliminated": "Не использован"
}

branch_id_color = {
    '00000000146887': '#d1e7dd',  # Марьина Роща :: зеленый
    '00000000172389': '#ffc99c',  # Котельники :: оранжевый
    '00000000279052': '#fff3cd',  # ПМ-Фарма :: песочный
    '00000000183929': '#cfe2ff',  # Санк-Петербург :: голубой
    '00000000413937': '#cff4fc',  # ПМ-Ритейл (Москва) :: берюзовый
    '00000000462867': '#cff4fc',  # ПМ-Ритейл (Санк-Петербург) :: берюзовый
    '': '#f8d7da'  # Отсутствует
}


class Kiz:
    def __init__(self):
        self.kiz: str  # Сам КИЗ (SGTIN или SSCC)
        self.parent: str  # Коробка / Паллет, в которой лежит КИЗ
        self.name: str  # Наименование ЛП (актуально для SGTIN: sell_name + prod_name)
        self.status: str  # Статус
        self.status_rus: str  # Статус (русифицировано)
        self.mod: str  # Место деятельности
        self.mod_address: str  # Адрес
        self.mod_guid: str  # GUID Адреса
        self.mod_color: str  # Цвет адреса для выделения в приложениях
        self.owner: str  # Контрагент
        self.owner_inn: str  # ИНН Контрагента
        self.owner_sys_id: str  # SYS_ID Контрагента
        self.batch: str  # Серия
        self.expiration_date: str  # Срок годности
        self.error_code: str  # Код ошибки
        self.error_desc: str  # Сообщение ошибки
        self.is_archive: str  # Данные из архива

        # Актуально только для SSCC
        self.sscc_count: str  # Кол-во КИЗ в SSCC
        self.sscc_last_date: str  # Дата последней совершенной операции
        self.sscc_status_date: str  # Дата статуса

        # Актуально только для SGTIN
        self.sgtin_prod_d_name: str  # Дозировка
        self.sgtin_prod_form_name: str  # Форма выпуска
        self.sgtin_reg_holder: str  # Держатель Р.У. + данные (reg_number + reg_date)
        self.sgtin_drug_code: str  # Идентификатор в ЕСКЛП

    def fillSgtin(self, sg: Sgtin):
        self.kiz = sg.sgtin
        self.parent = sg.sscc
        self.name = sg.name()
        self.status = sg.status
        self.mod = sg.branch_id
        self.batch = sg.batch
        self.expiration_date = sg.expiration_date

        self.sgtin_prod_d_name = sg.prod_d_name
        self.sgtin_prod_form_name = sg.prod_form_name
        self.sgtin_reg_holder = sg.reg_holder
        self.sgtin_drug_code = sg.drug_code

        self.fillStatus()

    def fillSscc(self, ss: Sscc):
        self.kiz = ss.sscc
        self.parent = ss.parent_sscc
        self.status = ss.status
        self.mod = ss.owner_id
        self.error_code = ss.error_code
        self.error_desc = ss.error_desc

        self.sscc_count = ss.count
        self.sscc_last_date = ss.last_tracing_op_date
        self.sscc_status_date = ss.status_date

        self.fillStatus()

    def fillModFromList(self, mod_list):
        for mod in mod_list:
            if self.mod == mod['MOD']:
                self.fillMod(mod)
                return

    def fillMod(self, mod_info: dict[str, str]):
        def x(field):
            if field in mod_info:
                return mod_info[field]
            else:
                return ''

        def get_color():
            if self.mod in branch_id_color:
                return branch_id_color[self.mod]
            return ''

        if mod_info is None:
            return

        self.mod_address = x('ADDRESS_NAME')
        self.mod_guid = x('ADDRESS_GUID')
        self.mod_color = get_color()
        self.owner = x('NAME')
        self.owner_inn = x('INN')
        self.owner_sys_id = x('SYS_ID')

    def fillStatus(self):
        if self.status in status_kiz:
            self.status_rus = f'{status_kiz[self.status]} ({self.status})'
        else:
            self.status_rus = ''

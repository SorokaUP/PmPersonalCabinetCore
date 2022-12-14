class Sgtin:
    def __init__(self, item):
        def x(field):
            return str(item[field]) if field in item else ''

        self.prod_name = x('prod_name')
        self.sell_name = x('sell_name')
        self.prod_d_name = x('prod_d_name')
        self.prod_form_name = x('prod_form_name')
        self.batch = x('batch')
        self.expiration_date = x('expiration_date').replace('T00:00:00', '')
        self.sgtin = x('sgtin')
        self.reg_holder = x('reg_holder')
        self.reg_number = x('reg_number')
        self.reg_date = x('reg_date').replace('T00:00:00', '')
        self.drug_code = x('drug_code')
        self.status = x('status')
        self.branch_id = x('branch_id')
        self.emission_type = x('emission_type')
        self.total_sold_part = x('total_sold_part')
        self.total_withdrawal_part = x('total_withdrawal_part')
        self.sscc = x('sscc')

    def __str__(self):
        return self.sgtin

    def name(self):
        return f"{self.sell_name} ({self.prod_name})"

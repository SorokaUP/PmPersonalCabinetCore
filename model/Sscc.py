class Sscc:
    def __init__(self, item):
        def x(field):
            return str(item[field]) if field in item else ''

        self.sscc = x('sscc')
        self.owner_id = x('owner_id')
        self.status_date = x('status_date')
        self.last_tracing_op_date = x('last_tracing_op_date')
        self.status = x('status')
        self.count = x('count')
        self.parent_sscc = x('parent_sscc')
        self.error_code = x('error_code')
        self.error_desc = x('error_desc')

    def __str__(self):
        return self.sscc

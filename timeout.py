from time import sleep
from datetime import datetime, timedelta


class TimeOutInfo:
    def __init__(self, timeout_sec: float):
        self.last = datetime.now() + timedelta(days=-1)
        self.timeout_sec = timeout_sec

    def __check_timeout(self):
        def convert_time(dtm: datetime):
            return datetime.fromtimestamp(dtm.timestamp())

        local_time = convert_time(datetime.now())
        last_time = convert_time(self.last)

        time_delta = local_time - last_time
        return self.timeout_sec >= time_delta.total_seconds()

    def timeout(self):
        if self.__check_timeout():
            sleep(self.timeout_sec)
            self.last = datetime.now()


method_timeout = {
    'default': TimeOutInfo(0.5),
    'reestr/sgtin/public/sgtins-by-list': TimeOutInfo(0.5),
}

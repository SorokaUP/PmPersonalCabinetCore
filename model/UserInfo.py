from db import mapper as db
from auth import auth
from datetime import datetime


class UserInfo:
    def __init__(self, data):
        self.client_id = data[0]
        self.client_secret = data[1]
        self.user_id = data[2]
        self.auth_type = 'SIGNED_CODE'
        self.thumbprint: str = data[3]

        # region Properties
        self.__token = ''
        self.__token_time = datetime.min
        self.__token_limit_seconds = 25 * 60  # 25 минут (хоть и утверждается что 30 минут простоя)
        # endregion

    def __str__(self):
        return self.user_id

    # Конвертируем для получения токена
    def todict(self):
        return {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'user_id': self.user_id,
            'auth_type': self.auth_type
        }

    # Проверяем токен на истечение срока
    def __token_time_is_up(self) -> bool:
        def convert_time(dtm: datetime):
            return datetime.fromtimestamp(dtm.timestamp())

        local_time = convert_time(datetime.now())
        token_time = convert_time(self.__token_time)

        token_time_delta = local_time - token_time
        return token_time_delta.total_seconds() >= self.__token_limit_seconds

    # Получить актуальный токен
    def get_token(self, is_forced=False) -> str:
        # Первичный запрос токена из базы данных
        if self.__token == '':
            self.__init_token()

        # Проверяем актуальность токена
        if self.__token_time_is_up() or is_forced:
            self.__update_token()

        return self.__token

    # Первичный запрос токена
    def __init_token(self):
        token_data = db.getToken(self.user_id)
        self.__token = str(token_data[0]).replace('None', '')
        self.__token_time = token_data[1]

    # Обновление токена
    def __update_token(self):
        self.__token = auth(self.user_id, self.todict(), self.thumbprint)  # Получаем новый токен
        db.updateToken(self.user_id, self.__token)  # Обновляем в базе данных
        self.__token_time = datetime.now()  # Обновляем время токена

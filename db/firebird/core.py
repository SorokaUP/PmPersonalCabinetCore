from firebird.driver import connect, driver_config, Cursor
from .model import FbDatabaseMetadata


def getDatabaseMetadata(alias):
    data = FbDatabaseMetadata()
    if alias == 'mdlp':
        data.alias = alias
        data.host = '192.168.127.30'
        data.user = 'SYSDBA'
        data.password = 'dbsrv'

    return data


def getCursor(alias):
    dbInfo = getDatabaseMetadata(alias)
    driver_config.server_defaults.host.value = dbInfo.host
    con = connect(dbInfo.alias, user=dbInfo.user, password=dbInfo.password, no_gc=True)
    cur = con.cursor()
    return cur


def endCursor(cur, tr='commit', close=False):
    cur.close()
    match tr.lower():
        case 'commit':
            cur.connection.commit()
    if close:
        cur.connection.close()


class fb:
    def __init__(self, alias):
        self.db_info = getDatabaseMetadata(alias)
        self.__connection = self.__getConnection()
        self.cursor: Cursor

    def __getConnection(self):
        driver_config.server_defaults.host.value = self.db_info.host
        con = connect(self.db_info.alias, user=self.db_info.user, password=self.db_info.password, no_gc=True)
        return con

    def prepare(self):
        if self.__connection.is_closed():
            self.__connection.begin()
        self.cursor = self.__connection.cursor()

    def commit(self):
        if not self.cursor.is_closed():
            self.cursor.close()
        if self.__connection.is_active():
            self.__connection.commit()

    def close(self):
        if not self.cursor.is_closed():
            self.cursor.close()
        if self.__connection.is_active():
            self.__connection.close()

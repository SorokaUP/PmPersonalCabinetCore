from .core import fb


__dbMdlp = fb('mdlp')


def getCounteragentInfo(branch_id: str):
    __dbMdlp.prepare()
    fld = ['NAME', 'INN', 'SYS_ID', 'ADDRESS_NAME', 'ADDRESS_GUID']
    __dbMdlp.cursor.execute(f"select {','.join(fld)} from sp$counteragent_mod_sel('{branch_id}');")
    res = __dbMdlp.cursor.fetchone()
    __dbMdlp.commit()
    return res, fld


def CLOSE():
    __dbMdlp.close()

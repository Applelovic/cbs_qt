from sqlalchemy import create_engine

from cbsqt.data.utils.db_config import DBConnectionInfo
# from cbaasquant.data.utils.tool import Base

__all__ = ['Engine']


class EnginePrefix:
    MySQL = 'mysql+pymysql'
    Oracle = 'oracle'


class EngineBulder(object):

    def __init__(self, dbconfig):
        self._host = getattr(dbconfig, 'host', RuntimeError)
        self._user = getattr(dbconfig, 'user', RuntimeError)
        self._password = getattr(dbconfig, 'password', RuntimeError)
        self._port = getattr(dbconfig, 'port', RuntimeError)
        self._type = getattr(dbconfig, 'type', RuntimeError)
        self._schemas = getattr(dbconfig, 'schemas', RuntimeError)
        self._prefix = self._get_prefix(self._type)

    @staticmethod
    def _get_prefix(db_type):
        return getattr(EnginePrefix, db_type)

    @property
    def _engine_config(self):
        return '{pre}://{user}:{passwd}@{host}:{port}'.format(
            pre=self._prefix,
            user=self._user,
            passwd=self._password,
            host=self._host,
            port=self._port,
        )

    @property
    def engine(self):
        return create_engine(self._engine_config, encoding='utf-8', pool_size=20, max_overflow=0)


class Engine:
    lu_cbaas_dev = EngineBulder(DBConnectionInfo.lu_cbaas_dev).engine
    lu_cbaas_test = EngineBulder(DBConnectionInfo.lu_cbaas_test).engine
    sycamore_cbaas_prod = EngineBulder(DBConnectionInfo.lu_cbaas_dev).engine


if __name__ == '__main__':
    print(Engine.lu_cbaas_test)

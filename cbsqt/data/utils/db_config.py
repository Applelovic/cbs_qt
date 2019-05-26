# -*- coding: utf-8 -*-
__all__ = ['DBConnectionInfo']


class ConfigElement(object):

    def __init__(self, config_dict=None):

        config = {
            'host': '',
            'user': '',
            'password': '',
            'port': '',
            'type': '',
            'schemas': ''
        }
        if config_dict:
            config.update(config_dict)
        self.__dict__ = config

    def __repr__(self):
        return '{}'.format('\n'.join(["{}: {}".format(k, v) for k, v in self.__dict__.items()]))


class DBType(object):
    MySQL = 'MySQL'
    Oracle = 'Oracle'


class Schemas:
    LuCBAASDev = ['barra', 'cbaasquant', 'cbaas_quant', 'cbsdata', 'quant',
                  'suntime', 'sycamore', 'wind', 'wind_from_lu_oracle']
    SycamoreProd = ['barra', 'cbaasquant', 'quant', 'suntime', 'sycamore',
                    'wind', 'wind_from_lu_oracle']


class DBConnectionConfig:
    lu_cbaas_dev = {
        'host': '172.23.30.115',
        'user': 'cbaas',
        'password': 'aNSQM88rSH',
        'port': 3306,
        'type': DBType.MySQL,
        'schemas': Schemas.LuCBAASDev
    }

    lu_cbaas_test = {
        'host': '172.19.46.31',
        'user': 'cbaas',
        'password': 'aNSQM88rSH',
        'port': 3306,
        'type': DBType.MySQL,
        'schemas': Schemas.LuCBAASDev
    }

    sycamore_cbaas_prod = {
        'host': '172.168.72.215',
        'user': 'lu',
        'password': 'w1a32j9XPc',
        'port': 3306,
        'type': DBType.MySQL,
        'schemas': Schemas.SycamoreProd
    }

    lu_wind_test = {
        'host': '172.16.112.183',
        'user': 'wind',
        'password': 'wind',
        'port': 1521,
        'type': DBType.Oracle
    }


class DBConnectionInfo:
    lu_cbaas_dev = ConfigElement(DBConnectionConfig.lu_cbaas_dev)
    lu_cbaas_test = ConfigElement(DBConnectionConfig.lu_cbaas_test)
    sycamore_cbaas_prod = ConfigElement(DBConnectionConfig.sycamore_cbaas_prod)
    lu_wind_test = ConfigElement(DBConnectionConfig.lu_wind_test)


if __name__ == '__main__':
    print(DBConnectionInfo.lu_cbaas_dev)

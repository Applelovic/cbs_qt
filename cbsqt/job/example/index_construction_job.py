from pandas import Timestamp, Series

from cbsqt.job.interface import AbstractJob

from cbsqt.data.utils.engine import Engine
from cbsqt.data.utils.tool import QueryTool
from cbsqt.data.source.wind import AShareEODPrices

__all__ = ['ConstructIndex']


class ConstructIndex(AbstractJob):

    def __init__(self, init_nav=1):
        self._init_nav = init_nav
        self._engine = Engine
        self._cur_time = None
        self._prv_nav = init_nav
        self._result = {}

    def set_time(self, time_obj=None):
        if time_obj:
            self._cur_time = time_obj

    def run_singal(self):
        # print(self._cur_time.date_.strftime('%Y-%m-%d'))
        return ord(self._cur_time.is_week_end) == 1

    def run_snapshot(self):
        date_str = self._cur_time.date_.strftime('%Y%m%d')
        equity1 = QueryTool(AShareEODPrices.S_DQ_PCTCHANGE, Engine.lu_cbaas_dev).\
            filter(AShareEODPrices.S_INFO_WINDCODE == '000001.SZ').\
            filter(AShareEODPrices.TRADE_DT == date_str).all()
        equity2 = QueryTool(AShareEODPrices.S_DQ_PCTCHANGE, Engine.lu_cbaas_dev).\
            filter(AShareEODPrices.S_INFO_WINDCODE == '601398.SH').\
            filter(AShareEODPrices.TRADE_DT == date_str).all()
        index_return = equity1[0][0] * 0.5 + equity2[0][0] * 0.5
        self._result.update({self._cur_time.date_: index_return})

    def termination(self):
        print(Series(self._result))

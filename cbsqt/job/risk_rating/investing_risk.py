
# from pandas import DataFrame

# from cbsqt.data.prod.cbaas import FundStatsHF, FundStatsMF, CBAASFund
from cbsqt.data.source.suntime import SuntimeFundInfo

from cbsqt.data.prod.cbaas import TradeCalendar
from cbsqt.data.utils.tool import QueryTool
from cbsqt.data.utils.engine import Engine

from cbsqt.job.interface import AbstractJob


class InvestingRiskHF(AbstractJob):

    def __init__(self):
        self._engine = Engine
        self._cur_time = QueryTool(TradeCalendar, self._engine.lu_cbaas_test.cbaas).\
            filter(TradeCalendar.date_ == '1990-12-31').all()[0]

        self._fund_info = None
        self._get_fund_info()

    def set_time(self, cur_time_obj=None):
        if cur_time_obj:
            print(cur_time_obj.date_)

    def run_singal(self):
        return ord(self._cur_time.is_month_end) == 1

    def run_snapshot(self):
        return

    def termination(self, cur_time_obj=None):
        if cur_time_obj:
            self._cur_time = cur_time_obj

    def _get_fund_info(self):
        # cbaas_fund_info = DataFrame(
        #     QueryTool([CBAASFund.S_INFO_WINDCODE.label('suntime_id'),
        #                CBAASFund.id.label('cbaas_id'),
        #                CBAASFund.strategy],
        #               self._engine.lu_cbaas_test.cbaasquant).all()
        # )
        #
        # suntime_fund_info = DataFrame(
        #     QueryTool([SuntimeFundInfo.fund_id.label('suntime_id'),
        #                SuntimeFundInfo.fund_name.label('fund_name'),
        #                SuntimeFundInfo.foundation_date.label('foundation_date')],
        #               self._engine.lu_cbaas_test.suntime)
        # )
        # self._fund_info = cbaas_fund_info.merge(suntime_fund_info,
        #                                         on='',)
        info = QueryTool([CBAASFund.S_INFO_WINDCODE.label('suntime_id'),
                          CBAASFund.id.label('cbaas_id'),
                          CBAASFund.strategy,
                          SuntimeFundInfo.fund_id.label('suntime_id'),
                          SuntimeFundInfo.fund_name.label('fund_name'),
                          SuntimeFundInfo.foundation_date.label('foundation_date')],
                         self._engine.lu_cbaas_dev).\
            join(CBAASFund.S_INFO_WINDCODE == SuntimeFundInfo.fund_id).all()
        self._fund_info = info




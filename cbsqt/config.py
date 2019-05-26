from pandas import DataFrame

from cbsqt.data.prod.cbaas import TradeCalendar
from cbsqt.data.utils.tool import QueryTool
from cbsqt.data.utils.engine import Engine


class TimeAxis(object):

    def __init__(self, start, end):
        self._engine = Engine
        self._axis = QueryTool([TradeCalendar.date_,
                                TradeCalendar.prev_trade_date,
                                TradeCalendar.is_open,
                                TradeCalendar.is_week_end,
                                TradeCalendar.is_month_end,
                                TradeCalendar.is_quarter_end,
                                TradeCalendar.is_year_end,
                                TradeCalendar.cal_end_of_month],
                               self._engine.lu_cbaas_dev).\
            filter(TradeCalendar.date_ >= start).\
            filter(TradeCalendar.date_ < end).all()

    @property
    def axis_view(self):
        return DataFrame(self._axis)

    @property
    def elements(self):
        return self._axis


if __name__ == '__main__':
    print(TimeAxis('2018-01-01', '2018-01-31').axis_view)

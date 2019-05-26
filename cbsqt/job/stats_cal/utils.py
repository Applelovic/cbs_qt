from pandas import Timestamp
from itertools import groupby


class TimeAxisCutter(object):

    def __init__(self, axis):
        self._axis = [Timestamp(ts) for ts in axis]
        self._axis.sort()
        self._cur_date = self._axis[-1]
        self._cur_year = self._cur_date.year
        self._cur_month = self._cur_date.month
        self._cur_quarter = self._cur_date.quarter
        self._cur_week = self._cur_date.week
        self._cur_yearweek = self._cur_year*1000 + self._cur_week
        self._cur_yearmonth = self._cur_year*100 + self._cur_month
        self._cur_yearquarter = self._cur_year*10 + self._cur_quarter
        self._cur_yearyear = self._cur_year * 0 + self._cur_year

        self._section_settings = {'w': ('week', 1000),
                                  'm': ('month', 100),
                                  'q': ('quarter', 10),
                                  'y': ('year', 0)}

    def inception(self):
        for _ in range(len(self._axis)):
            yield True

    def current_section(self, unit='w'):
        if unit not in self._section_settings:
            raise ValueError('Invalid section unit {w!r}. Please choose among {choices!r}.'.
                             format(w=unit, choices=('w', 'm', 'q', 'y')))
        suffix, multiple = self._section_settings[unit]
        determinator = self.__getattribute__('_cur_year{}'.format(suffix))

        for ts in self._axis:
            ts_chooser = getattr(ts, suffix)
            yield ts.year*multiple + ts_chooser == determinator

    def recent_n_weeks(self, n=1):
        for ts in self._axis:
            yield ts.year * 1000 + ts.week - self._cur_yearweek < n

    def recent_n_months(self, n=1):
        for ts in self._axis:
            yield ts.year * 100 + ts.month - self._cur_yearmonth < n

    def recent_n_quarters(self, n=1):
        for ts in self._axis:
            yield ts.year * 10 + ts.quarter - self._cur_yearquarter < n

    def recent_n_years(self, n=1):
        for ts in self._axis:
            yield ts.year - self._cur_year < n

    def mthly(self, m='w'):
        suffix, _ = self._section_settings[m]
        for _, group in groupby(self._axis, lambda ts: ts.year + getattr(ts, suffix)):
            axis_range = list(group)
            yield self._axis.index(axis_range[0]), self._axis.index(axis_range[-1])
            # yield self._axis.index(list(group)[0]), self._axis.index(list(group)[-1])


if __name__ == '__main__':
    from cbaasquant.data.prod.cbaas import TradeCalendar
    from cbaasquant.data.utils.engine import Engine
    from cbaasquant.data.utils.tool import QueryTool
    from pandas import DataFrame

    engine = Engine.lu_cbaas_dev
    test_date = DataFrame(QueryTool(TradeCalendar.date_, engine).limit(20).all())
    cutter = TimeAxisCutter(test_date.iloc[:, 0])
    for i in list(cutter.mthly('w')):
        print(i)

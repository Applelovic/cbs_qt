from numpy import empty, vstack

from cbsqt.job.stats_cal.utils import TimeAxisCutter
from cbsqt.mathlib.statistics import Indicators


def win_ratio(return_arr, timeaxis, by='w', **kwargs):
    mthly_cum_return = empty((0, return_arr.shape[1]))
    for s, e in TimeAxisCutter(timeaxis).mthly(by):
        mthly_cum_return = vstack((mthly_cum_return,
                                  Indicators.cumulative_return(return_arr[s:e, :], **kwargs)))
    winratio = Indicators.winning_ratio(mthly_cum_return)
    return winratio


if __name__ == '__main__':
    from cbaasquant.job.stats_cal.data_tool import get_fund_performance
    from pandas import DataFrame
    from numpy import ma
    from cbaasquant.data.utils.engine import Engine

    eng = Engine.lu_cbaas_dev
    raw_data = get_fund_performance(eng, start='2018-01-01', end='2018-03-31', freq='d')
    aligned = DataFrame(raw_data).pivot('date', 'fund_id', 'return')
    time_aixs = aligned.index
    ma_array = ma.array(aligned, mask=aligned.isnull())

    winR = win_ratio(ma_array, time_aixs, by='m')

    print(winR)

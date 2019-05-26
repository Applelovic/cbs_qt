from cbsqt.job.stats_cal.cal_job import IndicatorsCal
from cbsqt.main import run

if __name__ == '__main__':
    run('2001-01-01', '2018-08-01', [IndicatorsCal('MF', '2018-01-01')])

from sqlalchemy import func

from cbsqt.data.utils.tool import QueryTool
from cbsqt.data.prod.cbaas import CBAASFund, DailyPerformance, WeeklyPerformance, MonthlyPerformance


def _get_fund_type(ftype=None):
    ftype_dic = {'HF': [8],
                 'MF': [10]}

    if ftype is None:
        type_cond = [8, 10]
    elif ftype in ftype_dic:
        type_cond = ftype_dic[ftype]
    else:
        raise NotImplementedError('Fund type {!r} has not been implemented.'.format(ftype))

    return type_cond


def get_fund_info(engine, ftype=None):

    fund_types = _get_fund_type(ftype)

    return QueryTool([CBAASFund.id.label('fund_id'),
                      CBAASFund.S_INFO_WINDCODE,
                      CBAASFund.asset_class,
                      CBAASFund.inception_date,
                      CBAASFund.latest_nav_date],
                     engine).\
        filter(CBAASFund.valid == 1).\
        filter(CBAASFund.asset_class.in_(fund_types)).\
        all()


def _get_config_params(performance_table, engine, ftype=None, fund_id=None, start=None, end=None):
    fund_types = _get_fund_type(ftype)

    if fund_id is None:
        funds = [_id for _id, in QueryTool(CBAASFund.id, engine).filter(CBAASFund.asset_class.in_(fund_types)).filter(
            CBAASFund.valid == 1).all()]
    elif not isinstance(fund_id, list):
        funds = list(fund_id)
    else:
        funds = fund_id

    if not start:
        start_date = QueryTool(func.min(performance_table.date_), engine).\
            filter(performance_table.fund_id.in_(funds)).\
            scaler().\
            strftime('%Y-%m-%d')
    else:
        start_date = start

    if not end:
        end_date = QueryTool(func.max(performance_table.date_), engine). \
            filter(performance_table.fund_id.in_(funds)). \
            scaler(). \
            strftime('%Y-%m-%d')
    else:
        end_date = end

        return funds, start_date, end_date


def get_fund_performance(engine, ftype='MF', fund_id=None, start=None, end=None, freq='d', date_col='date'):
    if freq not in ['d', 'w', 'm']:
        raise ValueError('{!r} is not in frequency options ("d", "w", "m").'.format(freq))

    if freq == 'd':
        table = DailyPerformance
        funds, start_date, end_date = _get_config_params(table, engine, ftype, fund_id, start, end)
        performance = QueryTool([DailyPerformance.fund_id,
                                 DailyPerformance.date_.label(date_col),
                                 (DailyPerformance.return_/100).label('return')],
                                engine).\
            filter(DailyPerformance.fund_id.in_(funds)).\
            filter(DailyPerformance.date_ <= end).\
            filter(DailyPerformance.date_ > start).\
            all()
    elif freq == 'w':
        table = WeeklyPerformance
        funds, start_date, end_date = _get_config_params(table, engine, ftype, fund_id, start, end)
        performance = QueryTool([WeeklyPerformance.fund_id,
                                 WeeklyPerformance.month_end.label(date_col),
                                 (WeeklyPerformance.return_/100).label('return')],
                                engine).\
            filter(WeeklyPerformance.fund_id.in_(funds)).\
            filter(WeeklyPerformance.month_end <= end).\
            filter(WeeklyPerformance.month_end > start).\
            all()
    elif freq == 'm':
        table = MonthlyPerformance
        funds, start_date, end_date = _get_config_params(table, engine, ftype, fund_id, start, end)
        performance = QueryTool([MonthlyPerformance.fund_id,
                                 MonthlyPerformance.month_end.label(date_col),
                                 (MonthlyPerformance.return_/100).label('return')],
                                engine).\
            filter(MonthlyPerformance.fund_id.in_(funds)).\
            filter(MonthlyPerformance.month_end <= end).\
            filter(MonthlyPerformance.month_end > start).\
            all()
    else:
        raise NotImplementedError('Performance table with frequency of {!r} has yet implemented.'.format(freq))

    return performance


if __name__ == '__main__':
    from cbaasquant.data.utils.engine import Engine

    eng = Engine.lu_cbaas_dev
    # test = get_fund_performance(engine=eng, ftype='HF', start='2018-01-01', end='2018-01-08', freq='w')
    # from pandas import DataFrame
    # print(DataFrame(test))

    test = QueryTool([CBAASFund.id,
                      CBAASFund.asset_class,
                      CBAASFund.inception_date,
                      CBAASFund.latest_nav_date],
                     eng). \
        filter(CBAASFund.id == 473247). \
        all()

    print(test)

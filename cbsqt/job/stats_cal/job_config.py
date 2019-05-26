from cbsqt.mathlib.statistics import Indicators
from cbsqt.job.stats_cal.calculators import win_ratio

WindowCutterConfig = {'ITD': {'method': 'inception'},
                      'YTD': {'method': 'current_section',
                              'kwargs': {'unit': 'y'}
                              },
                      'QTD': {'method': 'current_section',
                              'kwargs': {'unit': 'q'}
                              },
                      'MTD': {'method': 'current_section',
                              'kwargs': {'unit': 'y'}
                              },
                      'WTD': {'method': 'current_section',
                              'kwargs': {'unit': 'y'}
                              },
                      '1m': {'method': 'recent_n_months',
                             'kwargs': {'n': 1}
                             },
                      '3m': {'method': 'recent_n_months',
                             'kwargs': {'n': 3}
                             },
                      '6m': {'method': 'recent_n_months',
                             'kwargs': {'n': 6}
                             },
                      '1y': {'method': 'recent_n_months',
                             'kwargs': {'n': 1}
                             },
                      '2y': {'method': 'recent_n_months',
                             'kwargs': {'n': 8}
                             },
                      '3y': {'method': 'recent_n_months',
                             'kwargs': {'n': 3}
                             },
                      '5y': {'method': 'recent_n_months',
                             'kwargs': {'n': 5}
                             }
                      }

CalWindows = {'group1': ['ITD', 'YTD', 'QTD', 'MTD', 'WTD', '1m', '3m', '6m', '1y', '2y', '3y', '5y'],
              'group2': ['1m', '3m', '6m', '1y', '2y', '3y', '5y']}


ReturnSeriesCalIndicators = {'cum_return': {'func': Indicators.final_cumulative_return,
                                            'kwargs': {'axis': 0}
                                            },
                             'annulized_return': {'func': Indicators.annualized_return,
                                                  'kwargs': {'multiplier': {'MF': 252, 'HF': 52}, 'axis': 0},
                                                  },
                             'annulized_vol': {'func': Indicators.annualized_vol,
                                               'kwargs': {'multiplier': {'MF': 252, 'HF': 52}, 'axis': 0}
                                               },
                             'winRatio_byWeek': {'func': win_ratio,
                                                 'kwargs': {'timeaxis': None, 'by': 'w'}},
                             'winRatio_byMonth': {'func': win_ratio,
                                                  'kwargs': {'timeaxis': None, 'by': 'm'}},
                             'winRatio_byQuarter': {'func': win_ratio,
                                                    'kwargs': {'timeaxis': None, 'by': 'q'}},
                             'winRatio_byYear': {'func': win_ratio,
                                                 'kwargs': {'timeaxis': None, 'by': 'y'}}
                             }

ReturnSeries = {'name': 'Return Series',
                'functions': ReturnSeriesCalIndicators,
                'cal_window': CalWindows['group1'],
                'value_accepter': 'ind_return_series',
                'rank_accepter': 'ind_return_series_ranking'}

FixedInvest = {'name': 'Fixed Invest',
               'functions': '',
               'cal_window': CalWindows['group1'],
               'accepter': 'ind_fixed_inv'}

Statstistics = {'name': 'Statstistics',
                'functions': '',
                'cal_window': CalWindows['group1'],
                'accepter': 'ind_statistical'}



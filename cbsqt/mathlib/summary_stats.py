# -*- coding: utf-8 -*-
from .statistics import Indicators

import numpy as np
import pandas as pd


class summary_stats():

    def __init__(self, return_frame, annual_risk_free_rate=0.02, confidence_level=0.05, annualization_multiplier=252):
        self.__data = np.array(return_frame)
        self.__rf = Indicators.frequency_transformation(annual_risk_free_rate, 1 / annualization_multiplier)
        self.__alpha = confidence_level
        self.__multi = annualization_multiplier
        self.__index = return_frame.index
        self.__columns = return_frame.columns

    @property
    def all_stats(self):

        basic_param = {'return_arr':self.__data,
                       'axis':0}

        annualized_param = {'return_arr': self.__data,
                            'multiplier': self.__multi,
                            'axis': 0}

        tail_risk_param = {'return_arr': self.__data,
                           'alpha': self.__alpha,
                           'axis': 0}

        absolute_param = {'return_arr': self.__data,
                          'risk_free_arr': self.__rf,
                          'multiplier': self.__multi,
                          'axis': 0}

        stats_dict = {}

        stats_dict.update({'cumulative_return': Indicators.final_cumulative_return(**basic_param)})
        stats_dict.update({'first_order_autocorrelation': Indicators.first_order_autocorrelation(**basic_param)})
        stats_dict.update({'annualized_return': Indicators.annualized_return(**annualized_param)})
        stats_dict.update({'annualized_volitility': Indicators.annualized_vol(**annualized_param)})
        stats_dict.update({'average_return': Indicators.average_return(**basic_param)})
        stats_dict.update({'return_median': Indicators.return_median(**basic_param)})
        stats_dict.update({'skewness': Indicators.skewness(**basic_param)})
        stats_dict.update({'kurtosis': Indicators.kurtosis(**basic_param)})
        stats_dict.update({'winning_ratio': Indicators.winning_ratio(**basic_param)})
        stats_dict.update({'sharpe_ratio': Indicators.sharpe(**absolute_param)})
        stats_dict.update({'sortino_ratio': Indicators.sortino(**absolute_param)})
        stats_dict.update({'calmar_ratio': Indicators.calmar(**absolute_param)})
        stats_dict.update({'max_drawdown': Indicators.max_drawdown(**basic_param)})
        stats_dict.update({'d4_drawdown_ration': Indicators.d4_drawdown_ratio(**absolute_param)})
        stats_dict.update({'d5_drawdown_ration': Indicators.d5_drawdown_ratio(**absolute_param)})
        stats_dict.update({'r3_drawdown_ration': Indicators.r3_drawdown_ratio(**absolute_param)})


        # stats_dict.update({'max_drawdown_duration': indicators.draw_down_duration(**basic_param)})

        longest_growing, longest_falling = Indicators.longest_continuations(**basic_param)
        stats_dict.update({'longest_growing': longest_growing})
        stats_dict.update({'longest_falling': longest_falling})
        stats_dict.update({'VaR': Indicators.VaR(**tail_risk_param)})
        stats_dict.update({'CVaR': Indicators.CVaR(**tail_risk_param)})
        stats_dict.update({'tail_risk': Indicators.tailRisk(**tail_risk_param)})
        stats_dict.update({'down_side_risk': Indicators.down_side_risk(**annualized_param)})
        stats_dict.update({'up_side_risk': Indicators.up_side_risk(**annualized_param)})

        stats = pd.DataFrame(stats_dict, index=self.__columns)

        return stats.transpose()

    def formalized(self, order=None, **mapping):

        default_mapping ={'cumulative_return': '累计收益率%',
                          'annulized_return': '年化收益率%',
                          'annulized_volitility': '年化波动率',
                          # 'average_return': '平均收益率%',
                          'skewness': '峰度',
                          'kurtosis': '偏度',
                          'sharpe_ratio': '夏普比率',
                          'sortino_ratio': '索提诺比率',
                          'calmar_ratio': '卡玛比率',
                          'winning_ratio': '胜率%',
                          'max_drawdown': '最大回撤%',
                          # 'max_drawdown_duration': '最大回撤持续时间',
                          'longest_growing': '最长连续上涨时间',
                          'longest_falling': '最长连续下跌时间',
                          'VaR': 'VaR',
                          'CVaR': 'CVaR',
                          'tail_risk':'尾部风险',
                          'down_side_risk': '下行风险',
                          'up_side_risk': '上行风险'
                          }

        default_mapping.update(**mapping)
        mapping_frame = pd.DataFrame(default_mapping, index=['指标']).transpose()

        default_order = ['cumulative_return', 'annulized_return', #'average_return',
                         'annulized_volitility', 'skewness', 'kurtosis', 'sharpe_ratio',
                         'sortino_ratio', 'calmar_ratio', 'winning_ratio', 'max_drawdown',
                         'longest_growing', 'longest_falling', #'max_drawdown_duration',
                         'VaR', 'CVaR', 'tail_risk', 'down_side_risk', 'up_side_risk']

        indicators_in_percentile = ['cumulative_return', 'annulized_return', #'average_return',
                                    'annulized_volitility', 'max_drawdown', 'winning_ratio',
                                    'VaR', 'CVaR', 'tail_risk', 'down_side_risk', 'up_side_risk']

        if order is not None:
            default_order = order

        stats = self.all_stats
        stats.loc[indicators_in_percentile, :] *= 100
        stats = stats.join(mapping_frame)

        return stats.reindex(default_order).set_index('指标').round(2)


if __name__ == '__main__':

    #test
    test_returns = pd.DataFrame((np.random.rand(200,2)-0.45)/10)
    print(summary_stats(test_returns).all_stats)
    print(summary_stats(test_returns).formalized())
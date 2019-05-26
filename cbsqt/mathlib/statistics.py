# -*- coding: utf-8 -*-

import numpy as np
import numpy.ma as ma
import scipy.stats as stats

# define new itemfreq here
# This itemfreq has the same output as np.itemfreq


def itemfreq(arr):
    uniqueright = np.unique(arr, return_counts=True)[1]
    right = uniqueright.reshape((len(np.unique(arr, return_counts=True)[1]), 1))
    uniqueleft = np.unique(arr, return_counts=True)[0]
    left = uniqueleft.reshape((len(np.unique(arr, return_counts=True)[1]), 1))
    return np.hstack((left, right))


class Indicators(object):
    
    def __init__(self):
        pass
    
    @staticmethod
    def best(return_arr, axis=0):
        return np.nanmax(return_arr, axis=axis)
    
    @staticmethod
    def worst(return_arr, axis=0):
        return np.nanmin(return_arr, axis=axis)

    @staticmethod
    def annualized_return(return_arr, multiplier=252, axis=0):
        return np.power(np.nanprod(return_arr + 1, axis=axis),
                        multiplier/return_arr.shape[0]) - 1

    @staticmethod  # coded by Alex Sun
    def return_median(return_arr, axis=0):
        return np.median(return_arr, axis=axis)
                        
    @staticmethod
    def annualized_vol(return_arr, multiplier=252, axis=0):
        return np.nanstd(return_arr, axis=axis) * np.sqrt(multiplier)
    
    @staticmethod
    def average_return(return_arr, axis=0):
        return np.nanmean(return_arr, axis=axis)
    
    @staticmethod
    def frequency_transformation(return_arr, multiplier=252/1):
        return np.power(1 + return_arr, multiplier) - 1 
    
    @staticmethod
    def cumulative_return(return_arr, axis=0):
        return np.nancumprod(return_arr + 1, axis=axis)
    
    @staticmethod
    def final_cumulative_return(return_arr, axis=0):        
        return Indicators.cumulative_return(return_arr, axis=axis)[-1] - 1

    @staticmethod
    def cumulative_max(return_arr, axis=0):
        cumulative_return = Indicators.cumulative_return(return_arr, axis=axis)
        return np.maximum.accumulate(cumulative_return, axis=axis)

    @staticmethod
    def draw_down(return_arr, axis=0):
        cumulative_return = Indicators.cumulative_return(return_arr, axis=axis)
        cumulative_max = Indicators.cumulative_max(return_arr, axis=axis)
        return np.divide(cumulative_return, cumulative_max) - 1
    
    @staticmethod
    def max_drawdown(return_arr, axis=0):
        draw_downs = Indicators.draw_down(return_arr, axis=axis)
        return np.nanmin(draw_downs, axis=axis)
    
    @staticmethod
    def _slice_draw_down_duration(return_arr, top=1, axis=0):
        
        nav = Indicators.cumulative_return(return_arr, axis=axis)
        high_water_marks = np.maximum.accumulate(nav, axis=axis)
        high_water_marks_counts = itemfreq(high_water_marks)
        high_water_marks_positions = np.argsort(high_water_marks_counts[:, -1], axis=axis)[-1*top]
        longest_cumulative_max = high_water_marks_counts[high_water_marks_positions, 0]
        max_draw_downs_durations = np.where(high_water_marks == longest_cumulative_max)[0]
        
        return max_draw_downs_durations.min(), max_draw_downs_durations.max()    
    
    @staticmethod
    def draw_down_range(return_arr, axis=0, top=1):
        return np.apply_along_axis(Indicators._slice_draw_down_duration,
                                   axis=axis,
                                   arr=return_arr,
                                   top=top)

    @staticmethod
    def draw_down_duration(return_arr, axis=0, top=1):
        start, end = np.apply_along_axis(Indicators._slice_draw_down_duration,
                                         axis=axis,
                                         arr=return_arr,
                                         top=top)
        return end - start
    
    @staticmethod
    def _continuation(return_arr):
                
        climbing_up = np.nancumsum(return_arr >= 0)
        climbing_down = np.nancumsum(return_arr < 0)
        continuous_growing_counts = itemfreq(climbing_down)
        continuous_falling_counts = itemfreq(climbing_up)
        
        return continuous_growing_counts[:, -1].max(), continuous_falling_counts[:, -1].max()
    
    @staticmethod
    def longest_continuations(return_arr, axis=0):
        return np.apply_along_axis(Indicators._continuation,
                                   axis=axis,
                                   arr=return_arr)
       
    @staticmethod
    def down_side_risk(return_arr, risk_free_arr=0, multiplier=252, axis=0):
        returns = return_arr - risk_free_arr
        returns[returns>0] = 0
        return np.nansum(np.power(returns, 2), axis=axis) * np.sqrt(multiplier)
    
    @staticmethod
    def up_side_risk(return_arr, risk_free_arr=0, multiplier=252, axis=0):
        returns = return_arr - risk_free_arr
        returns[returns<0] = 0
        return np.nansum(np.power(returns, 2), axis=axis) * np.sqrt(multiplier)
   
    @staticmethod
    def skewness(return_arr, axis=0):
        return np.array(stats.skew(return_arr, axis=axis, nan_policy='omit'))
    
    @staticmethod
    def kurtosis(return_arr, axis=0):
        return np.array(stats.kurtosis(return_arr, axis=axis, nan_policy='omit'))
    
    @staticmethod
    def winning_ratio(return_arr, axis=0):
        winning = np.nansum(return_arr > 0, axis=axis)
        total = return_arr.shape[axis]        
        return np.divide(winning, total)
  
    @staticmethod
    def VaR(return_arr, alpha=0.05, axis=0):
        return np.nanpercentile(return_arr, alpha*100, axis=axis)
    
    @staticmethod
    def CVaR(return_arr, alpha=0.05, axis=0):
        VaR = Indicators.VaR(return_arr, alpha=alpha, axis=axis)
        return np.nanmean(ma.array(return_arr, mask=return_arr > VaR), axis=axis)
   
    @staticmethod
    def tailRisk(return_arr, alpha=0.05, axis=0):
        VaR = Indicators.VaR(return_arr, alpha=alpha, axis=axis)
        return np.nanstd(ma.array(return_arr, mask=return_arr > VaR), axis=axis)
        
    @staticmethod
    def annualized_absolute_return(return_arr, risk_free_arr=0, multiplier=252, axis=0):
        return Indicators.annualized_return(return_arr - risk_free_arr,
                                            multiplier=multiplier,
                                            axis=axis)
    
    @staticmethod
    def sharpe(return_arr, risk_free_arr=0, multiplier=252, axis=0):
        absolute_return = Indicators.annualized_absolute_return(return_arr=return_arr,
                                                                risk_free_arr=risk_free_arr,
                                                                multiplier=multiplier,
                                                                axis=axis)
        annualized_volitility = Indicators.annualized_vol(return_arr=return_arr,
                                                          multiplier=multiplier,
                                                          axis=axis)
        return np.divide(absolute_return, annualized_volitility)
    
    @staticmethod
    def calmar(return_arr, risk_free_arr=0, multiplier=252, axis=0):
        absolute_return = Indicators.annualized_absolute_return(return_arr=return_arr,
                                                                risk_free_arr=risk_free_arr,
                                                                multiplier=multiplier,
                                                                axis=axis)
        max_draw_down = abs(Indicators.max_drawdown(return_arr=return_arr,
                                                    axis=axis))
        max_draw_down[max_draw_down == 0] = np.inf
        return np.divide(absolute_return, max_draw_down)
    
    @staticmethod
    def sortino(return_arr, risk_free_arr=0, multiplier=252, axis=0):
        absolute_return = Indicators.annualized_absolute_return(return_arr=return_arr,
                                                                risk_free_arr=risk_free_arr,
                                                                multiplier=multiplier,
                                                                axis=axis)
        down_side_risk = Indicators.down_side_risk(return_arr=return_arr,
                                                   multiplier=multiplier,
                                                   axis=axis)
        down_side_risk[down_side_risk == 0] = np.inf
        return np.divide(absolute_return, down_side_risk)
    
    @staticmethod
    def annualized_active_return(return_arr, bench_mark_arr, multiplier=252, axis=0):
        return Indicators.annualized_return(return_arr - bench_mark_arr,
                                            multiplier=multiplier,
                                            axis=axis)
    
    @staticmethod
    def annualized_active_vol(return_arr, bench_mark_arr, multiplier=252, axis=0):
        return Indicators.annualized_vol(return_arr - bench_mark_arr,
                                         multiplier=multiplier,
                                         axis=axis)
    
    @staticmethod
    def information_ratio(return_arr, bench_mark_arr, multiplier=252, axis=0):
        annualized_active_return = Indicators.annualized_active_return(return_arr=return_arr,
                                                                       bench_mark_arr=bench_mark_arr,
                                                                       multiplier=multiplier,
                                                                       axis=axis)
        annualized_active_vol = Indicators.annualized_active_vol(return_arr=return_arr,
                                                                 bench_mark_arr=bench_mark_arr,
                                                                 multiplier=multiplier,
                                                                 axis=axis)
        return np.divide(annualized_active_return, annualized_active_vol)

    @staticmethod  # coded by Alex Sun
    # calculate number, amplitude sum, amplitude mean of drawdowns
    def drawdown_parameter(return_arr, axis=0):
        draw_down=Indicators.draw_down(return_arr=return_arr, axis=axis)
        drawdown_sum = np.array([])  # sum of dd
        drawdown_number = np.array([])  # number of dd
        drawdown_mean = np.array([])  # mean of dd
        for j in np.arange(len(draw_down.T)):
            dd_mod = np.append(draw_down[:, j], 0)  # add 0 to the end of array to guarantee a complete block
            s = 0  # sign to show entrance and exit of block
            blk = 0  # number of dd for 1 column
            left = 0  # left boundaries of block
            dd_sum = 0  # sum of dd for 1 column
            for i in np.arange(len(dd_mod)):
                if dd_mod[i] != 0 and s == 0:  # enter blocks
                    s = (s + 1) % 2
                    blk = blk + 1
                    left = i
                elif dd_mod[i] == 0 and s != 0:  # leave block
                    s = (s + 1) % 2
                    dd_sum = dd_sum - np.nanmin(dd_mod[left:i + 1], axis=axis)
            drawdown_sum = np.append(drawdown_sum, dd_sum)
            drawdown_number = np.append(drawdown_number, blk)
            drawdown_mean = np.divide(drawdown_sum, drawdown_number)
        return drawdown_sum, drawdown_number, drawdown_mean

    @staticmethod  # coded by Alex Sun
    def d4_drawdown_ratio(return_arr, risk_free_arr=0, multiplier=252, axis=0):  # (R-Rf)/mean(dd)
        absolute_return = Indicators.annualized_absolute_return(return_arr=return_arr,
                                                                risk_free_arr=risk_free_arr,
                                                                multiplier=multiplier,
                                                                axis=axis)
        drawdown_sum, drawdown_number, drawdown_mean = Indicators.drawdown_parameter(return_arr=return_arr,
                                                                                     axis=axis)
        return np.divide(absolute_return, drawdown_mean)

    @staticmethod  # coded by Alex Sun
    def d5_drawdown_ratio(return_arr, risk_free_arr=0, multiplier=252, axis=0):  # (R-Rf)/sum(dd)
        absolute_return = Indicators.annualized_absolute_return(return_arr=return_arr,
                                                                risk_free_arr=risk_free_arr,
                                                                multiplier=multiplier,
                                                                axis=axis)
        drawdown_sum, drawdown_number, drawdown_mean = Indicators.drawdown_parameter(return_arr=return_arr,
                                                                                     axis=axis)
        return np.divide(absolute_return, drawdown_sum)

    @staticmethod  # coded by Alex Sun
    def r3_drawdown_ratio(return_arr, risk_free_arr=0, multiplier=252, axis=0, top=1):  # (R-Rf)/dd_duration
        absolute_return = Indicators.annualized_absolute_return(return_arr=return_arr,
                                                                risk_free_arr=risk_free_arr,
                                                                multiplier=multiplier,
                                                                axis=axis)
        dd_duration=Indicators.draw_down_duration(return_arr=return_arr,
                                                  axis=axis,
                                                  top=top)
        return np.divide(absolute_return, dd_duration)

    @staticmethod  # code by Alex Sun
    def first_order_autocorrelation(return_arr, axis=0):
        no_lag = np.delete(return_arr, -1, axis=0)
        lagged = np.delete(return_arr, 0, axis=0)
        tr_1 = no_lag-np.mean(no_lag, axis=axis)
        tr_2 = lagged - np.mean(lagged, axis=axis)
        denominator = np.sqrt(np.mean(np.square(tr_1), axis=0) * np.mean(np.square(tr_2), axis=axis))
        numerator = np.mean(tr_1 * tr_2, axis=axis)
        return np.divide(numerator, denominator)


if __name__ == '__main__':
    
    test_array = (np.random.rand(20, 2)-0.45)/10
    test_benchmark = (np.random.rand(40, 2)-0.55)/10
    test_nav = Indicators.cumulative_return(test_array)

    print(test_array)
    print(Indicators.draw_down(test_array))
    print(Indicators.drawdown_parameter(test_array))
    print(Indicators.d4_drawdown_ratio(test_array))
    print(Indicators.d5_drawdown_ratio(test_array))
    print(Indicators.r3_drawdown_ratio(test_array))
    print(Indicators.annualized_absolute_return(test_array))
    #print(Indicators.annualized_return_median(test_array))
    #print(Indicators.annualized_return(test_array))
    print(Indicators.first_order_autocorrelation(test_array))




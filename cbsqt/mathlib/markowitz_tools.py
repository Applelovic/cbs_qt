# -*- coding: utf-8 -*-
"""
Create at 2018/8/7

Usage:
    Markowitz Theroy

Refrence:
    - https://blog.csdn.net/matrix_laboratory/article/details/50821455
    - https://blog.csdn.net/qq_34941023/article/details/56513502

@author: Sue Zhu
"""
from cbsqt.mathlib.statistics import Indicators
from pandas import DataFrame
import numpy as np
from scipy.optimize import minimize

_freq_multplier = {'D': 252, 'W': 52, 'M': 12, 'Q': 4, 'Y': 1}


class MarkowitzTools(object):

    def __init__(self, ts_return: DataFrame, data_freq='W'):
        self.ts_return = ts_return

        self.cols = ts_return.columns.tolist()
        self.n_assets = ts_return.shape[1]
        self.freq = data_freq
        self.mul_ = _freq_multplier[self.freq]

        self._prt_cols = ['expected_return', 'expected_volitility'] + self.cols

    @property
    def cov_matrix(self):
        return self.ts_return.cov()

    @property
    def asset_ret(self):
        """ Use nick's indicator to calculate annualize return"""
        return Indicators.annualized_return(self.ts_return, self.mul_, axis=0)

    def prt_std(self, w):
        """ Calculate portfolio variance, `w` should be 1d array or pd.series. """
        return np.sqrt(np.dot(np.dot(w.T, self.cov_matrix), w) * self.mul_)

    def prt_ret(self, w):
        """ Calculate portfolio return, `w` should be 1d array or pd.series. """
        return np.dot(w.T, self.asset_ret)

    def min_variance(self, tar_ret, org_weight=None, w_bnds=None, ex_cons=None, opt_options=None):
        """ Given a target return, and return weight for minvariance. """
        if org_weight is None:
            org_weight = np.ones(self.n_assets) / self.n_assets

        cons = (
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # 所有参数(权重)的总和为1
            {'type': 'eq', 'fun': lambda x: self.prt_ret(x) - tar_ret}  # target_return
        )
        if ex_cons is not None:
            cons = cons + tuple(ex_cons)

        opt = minimize(self.prt_std, org_weight, method='SLSQP', bounds=w_bnds, constraints=cons, options=opt_options)
        calc_weight = opt.x
        return calc_weight

    def prt_random(self, sample_num=1000):
        """ Form portfolio with random weight."""
        # generate random weight
        weight = np.random.randint(0, 10, (self.n_assets, sample_num))
        weight = np.divide(weight, weight.sum(axis=0))

        # calculate stats
        rets = np.apply_along_axis(self.prt_ret, 0, weight)
        stds = np.apply_along_axis(self.prt_std, 0, weight)

        random_prt = DataFrame(np.vstack((rets, stds, weight)), index=self._prt_cols).T
        return random_prt

    def prt_eff_frt(self, sample_num=20, ret_bounds=None, ctrl_ineff=False, **kwargs):
        """ Form portfolio at efficient frontier with target returns and min variance.
        self.min_variance(tar_ret, org_weight=None, w_bnds=None, ex_cons=None, opt_options=None)"""
        if ret_bounds is None:
            ret_bounds = self.asset_ret.min(), self.asset_ret.max()
        tar_rets = np.linspace(*ret_bounds, sample_num)

        eff_points = []
        for tar in tar_rets:
            calc_weight = self.min_variance(tar, **kwargs)
            real_vol = self.prt_std(calc_weight)
            eff_points.append([tar, real_vol, *calc_weight])

        eff_front = DataFrame(eff_points, columns=self._prt_cols)

        var_diff = eff_front['expected_volitility'].diff()
        if ctrl_ineff and var_diff.lt(0).any():
            start_ret = eff_front.loc[var_diff.ge(0), 'expected_return'].iloc[0]
            if start_ret - ret_bounds[0] > 0.001:
                print("Adjust ret bounds at", start_ret)
                new_ret_bounds = start_ret, ret_bounds[1]
                return self.prt_eff_frt(sample_num, new_ret_bounds, **kwargs)
            else:
                return eff_front
        else:
            return eff_front

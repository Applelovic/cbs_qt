# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import statsmodels.api as sm
from itertools import combinations, takewhile, count
from datetime import datetime
from collections import OrderedDict
from sklearn.linear_model import LassoCV


def norm_ols(exog, endog, add_const, reg_kwags):
    """
    General ols function with package `statsmodels`, input exog(X) and endog(y)
    can be either np.ndarray else pd.Dataframe object.

    :param exog: X, dataframe with factor names as columns names
    :param endog: y, series of 1d array
    :param add_const: switch for adding constant in regression model.
    :param reg_kwags: other arguments for sm.OLS
    """





    if add_const:
        exog = sm.add_constant(exog)

    model = sm.OLS(endog, exog, **reg_kwags)
    results = model.fit()
    return results


class OLSLinearRegressor(object):

    def __init__(self, data: pd.DataFrame, add_constant=True, reg_kwags=None):
        self.data = data
        self.has_constant = add_constant
        self.reg_kwags = {} if reg_kwags is None else reg_kwags

        self._reg_result = self._fit()

    def _fit(self):
        x = self.data.iloc[:, 1:].copy()
        y = self.data.iloc[:, 0].copy()
        return norm_ols(x, y, self.has_constant, self.reg_kwags)

    def reg_res(self, name):
        return self._reg_result.__getattribute__(name)

    # model fitted
    @property
    def rsquared(self):
        return self._reg_result.rsquared

    @property
    def rsquared_adj(self):
        return self._reg_result.rsquared_adj

    @property
    def fvalue(self):
        return self._reg_result.fvalue

    @property
    def f_pvalue(self):
        return self._reg_result.f_pvalue

    @property
    def sigma(self):
        return np.std(self._reg_result.resid)

    # factor fitted
    @property
    def params(self):
        return self._reg_result.params

    @property
    def pvalues(self):
        return self._reg_result.pvalues


class LimitOLS(OLSLinearRegressor):
    def __init__(self, data: pd.DataFrame, add_constance=True, reg_kwags=None,
                 judge_param='rsquared_adj', n_limit: int = None, fast_mode: bool = False):
        """ Limit/Exhaust Algorithm of ols regression.
        :param n_limit: int, largest number of factors, if None, think it as Exhaust Algorithm
        :param fast_mode: bool, set it into True to stop when r2 decrease.
        """
        super().__init__(data, add_constance, reg_kwags)

        # params for limit
        self.judge = judge_param
        self.n_limit = data.shape[1] - 1 if n_limit is None else n_limit  # 选择的因子数
        self.fast = fast_mode  # when fast_mode is True, stop as adj_r2 decrease.

    def _fit(self):

        reg_result = list()
        judge_list = list()
        _reg_result = None
        y = self.data.iloc[:, 0].copy()

        for n_factor in range(1, self.n_limit + 1):
            judge_list.append(0)

            for factors in combinations(self.data.columns[1:], n_factor):
                arrX = self.data.loc[:, factors].copy()
                res_obj = norm_ols(arrX, y, **self.reg_kwags)
                res_judge = res_obj.__getattribute__(self.judge)

                reg_result.append({
                    'f_num': n_factor,
                    'factor_list': list(factors),
                    'res_obj': res_obj,
                    self.judge: res_judge
                })
                judge_list[-1] = max(judge_list[-1], res_judge)

                if _reg_result is None or res_judge > max(judge_list):
                    _reg_result = res_obj

            # When in "fast mode", stop when r2adj not increase.
            if self.fast and len(judge_list) > 1 and judge_list[-1] < judge_list[-2]:
                break

        return _reg_result


class _LoggerStepwise(object):
    def __init__(self):
        self.log_list = list()

    @property
    def summary(self):
        return pd.DataFrame(self.log_list).set_index('Time')

    def add_log(self, action, detail='', res=None):
        log_line = OrderedDict()
        log_line['Time'] = datetime.now()
        log_line['Action'] = action.capitalize()
        log_line['DetailMessage'] = detail

        if res is not None:
            log_line['Model_Rsq_Adj'] = res.rsquared_adj
            log_line['Model_Ftest_Prob'] = res.f_pvalue
            log_line['CurrentFactor'] = [f for f in res.model.exog_names if not 'const']

        self.log_list.append(log_line)


class StepwiseOLS(OLSLinearRegressor):
    def __init__(self, data: pd.DataFrame, add_constance=True, reg_kwags=None,
                 start_factor=None, tr_sim=0.9, tr_in=0.05, tr_out=0.05, limit_iter=100):
        """ Function for Stepwise OLS regression.
        :param tr_sim: float, p-value's thresh for drop indicator with correlation matrix.
        :param tr_in: float, p-value's thresh for forward step.
        :param tr_out: float, p-value's thresh for backward step.
        :param limit_iter: int, largest iter times for stepwise ols.
        """
        super().__init__(data, add_constance, reg_kwags)

        # params
        self.tr_sim = tr_sim
        self.tr_in = tr_in
        self.tr_out = tr_out
        self.limit_iter = limit_iter

        self._include_factors = start_factor if start_factor is not None else []
        self._indicator_factors = [c for c in self.data.columns[1:] if c not in self._include_factors]
        self._log = _LoggerStepwise()  # tmp attr initial empty before fit
        self.corr_mat = data.corr()

    @property
    def _y(self):
        return self.data.iloc[:, 0].copy()

    def _fit(self):
        res = None
        for c in count(1):
            # check iter limit
            if c > self.limit_iter:
                self._log.add_log(action='Break', detail='Iter times limit.')
                break

            # forward step
            new_factor, res = self._most_possible_feature()
            t_test = res.pvalues
            if t_test[new_factor] <= self.tr_in:
                # append new factor
                self._include_factors.append(new_factor)
                self._indicator_factors.remove(new_factor)
                self._log.add_log(
                    action='Append',
                    detail="{f} for p-value {p}".format(f=new_factor, p=t_test[new_factor]),
                    res=res)

                # decide drop indicator
                cov_slice = self.corr_mat.loc[self._include_factors, self._indicator_factors].stack()
                cov_over = cov_slice.ge(self.tr_sim).any().loc[lambda ser: ser]
                for f in cov_over.index:
                    self._indicator_factors.remove(f)
                    self._log.add_log(
                        action='Drop',
                        detail='{factor}, covariance {corr}'.format(corr=cov_slice.loc[:, f].to_dict(), factor=f))
            else:
                self._log.add_log(action='Break', detail='No valid indicator.')
                break

            # backward step
            if t_test.max() <= self.tr_out:
                for rm_f, rm_p in t_test.loc[lambda ser: ser > self.tr_out].iteritems():
                    self._include_factors.remove(rm_f)
                    self._log.add_log(action='Remove',
                                      detail='{factor}p-value {p}'.format(p=rm_p, factor=rm_f),
                                      res=res)

        if res is None:
            raise ValueError("Regression model can't be fitted with factor provided.")
        return res

    def _most_possible_feature(self):
        fw_reg_res = dict()
        for factor in self._indicator_factors:
            fw_test_factors = self._include_factors + [factor]
            fw_ols = norm_ols(self.data.loc[:, fw_test_factors].copy(), self._y, **self.reg_kwags)
            fw_reg_res[factor] = {'res': fw_ols, 'ttest_p': fw_ols.pvalues[factor]}

        new_feature = min(fw_reg_res, key=lambda f_ind: fw_reg_res[f_ind]['ttest_p'])
        return new_feature, fw_reg_res[new_feature]['res']

class LassoLinearReg(object):

    def __init__(self, data: pd.DataFrame, reg_kwags=None, n_alphas=100):
        self.data = data
        self.n_alphas = n_alphas
        self.reg_kwags = {} if reg_kwags is None else reg_kwags
        self._reg_result = self._fit()

    def _fit(self):
        X = self.data.iloc[:, 1:].copy()
        Y = self.data.iloc[:, 0].copy()
        return LassoCV(self.n_alphas)

    def reg_res(self, name):
        return self._reg_result.__getattribute__(name)







def _form_test_data():
    alpha = 0.3
    betas = np.arange(4)
    data = pd.DataFrame(np.random.randn(200, 5), columns=list('yabcd'))
    data['y'] = data.loc[:, 'a':].dot(betas).add(alpha) + 0.01 * np.random.randn(200)
    return data


if __name__ == '__main__':
    test_data = _form_test_data()
    ols = OLSLinearRegressor(data=test_data, add_constant=True)

    for attr in ['params', 'rsquared_adj', 'f_pvalue', 'pvalues']:
        print("Property '{}':\t{}".format(attr.capitalize(), ols.__getattribute__(attr)))



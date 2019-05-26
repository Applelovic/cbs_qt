from pandas import DataFrame, concat
from numpy import ma

from cbsqt.data.utils.engine import Engine
from cbsqt.job.interface import AbstractJob
from cbsqt.job.stats_cal.data_tool import get_fund_performance, get_fund_info
from cbsqt.job.stats_cal.utils import TimeAxisCutter
from cbsqt.job.stats_cal.job_config import WindowCutterConfig, CalWindows
from cbsqt.job.stats_cal.job_config import ReturnSeries


class IndicatorsCal(AbstractJob):

    def __init__(self, ftype=None, inception_start=None):
        self._cur_time = None
        self._prv_time = None
        self._fund_info = None
        self._raw_data_holder = None

        self._cal_window_config = CalWindows

        self._ftype = ftype
        self._inception_start = inception_start
        self._initialized = False

        self.registered_calculations = []
        self._eng = Engine.lu_cbaas_dev

    def calculation_registeration(self):
        self.registered_calculations.append(ReturnSeries)
        # self._registered_calculations.append(FixedInvest)
        # self._registered_calculations.append(Statstistics)
        print('Functions needed to be calculated are registed.')

    def set_time(self, time_obj):
        self._cur_time = time_obj
        pass

    @property
    def cur_time(self):
        if self._cur_time:
            return self._cur_time.date_.strftime('%Y-%m-%d')
        else:
            raise ValueError('Time object has not been injected.')

    @property
    def prv_time(self):
        if self._cur_time:
            return self._prv_time.date_.strftime('%Y-%m-%d')
        else:
            raise ValueError('Nothing has been passed to prv_time.')

    def run_singal(self):
        return ord(self._cur_time.is_week_end) == 1

    def run_snapshot(self):
        if self._initialized:
            self.data_subscription()
        else:
            self.data_initialization()
            self.calculation_registeration()

        print('{} is getting started.'.format(self.cur_time))
        current_valid_funds = list(self.get_snapshot_valid_fund())
        if self._raw_data_holder.__len__() > 0:
            aligned_data = DataFrame(self._raw_data_holder).pivot('date', 'fund_id', 'return').loc[:, current_valid_funds]
            self.function_processing(aligned_data)
            print('{} has been processed.'.format(self.cur_time))
        else:
            print('{} has not enough data.'.format(self.cur_time))
        self._prv_time = self._cur_time
        pass

    def termination(self):
        print('All finished with no bug.')
        pass

    def data_initialization(self):
        print('Initializing...({})'.format(self.cur_time))
        self._fund_info = get_fund_info(self._eng, ftype=self._ftype)
        self._raw_data_holder = get_fund_performance(self._eng,
                                                     ftype=self._ftype,
                                                     start=self._inception_start,
                                                     end=self.cur_time)
        self._initialized = True
        self._prv_time = self._cur_time
        print('Intialization completed.')

    @property
    def fund_info(self):
        return DataFrame(self._fund_info)

    def data_subscription(self):
        new_subscription = get_fund_performance(self._eng,
                                                ftype=self._ftype,
                                                start=self.prv_time,
                                                end=self.cur_time)
        self._raw_data_holder.extend(new_subscription)

    def get_snapshot_valid_fund(self):
        for ticker in self._fund_info:
            valid = (ticker.inception_date is None or ticker.inception_date <= self._cur_time.date_) and \
                    (ticker.latest_nav_date is None or ticker.latest_nav_date >= self._cur_time.date_)
            if valid:
                yield ticker.fund_id

    def function_processing(self, aligned_data):

        print('*Decomposing functions.')

        for function_config in self.registered_calculations:
            function_name = function_config['name']
            print('**Start Computing {}'.format(function_name))
            functions_2b_processed = function_config['functions']
            cal_window = function_config['cal_window']
            value_accepter = function_config['value_accepter']
            rank_accepter = function_config['rank_accepter']
            value, rank = self.single_function_processing(aligned_data, functions_2b_processed,
                                                          cal_window)
            print('**{} have been calculated.'.format(function_name))

            if value is not None:
                value.to_sql(con=self._eng, schema='cbaas', name=value_accepter,
                             if_exists='append', index=False, chunksize=1000)
                rank.to_sql(con=self._eng, schema='cbaas', name=rank_accepter,
                            if_exists='append', index=False, chunksize=1000)
                print('**{} have been uploaded.'.format(function_name))
            else:
                print('**Not enough data for {} on {}.'.format(function_name, self.cur_time))

    def single_function_processing(self, data, ind_config, windows):
        ind_value_list = []
        ind_rank_list = []

        # holder for all kwargs variables for all functions, need to be more generalized.
        variable_kwargs = {'timeaxis': data.index}

        for window in windows:
            print('***Processing {}'.format(window))
            cutter_config = WindowCutterConfig[window]
            cutter_kwargs = cutter_config['kwargs'] if 'kwargs' in cutter_config else {}
            axis_mask = getattr(TimeAxisCutter(data.index), cutter_config['method'])(**cutter_kwargs)
            nan_fitered = data.loc[axis_mask, :].dropna(how='all')
            valid = nan_fitered.loc[:, nan_fitered.count(axis=0) >= 24]
            if valid.shape[1] == 0:
                continue
            valid_funds = valid.columns
            valid_arr = ma.array(valid, mask=valid.isnull())
            indcators_value_result = {}
            indcators_rank_result = {}
            for key, config in ind_config.items():
                print('****Computing {}'.format(key))
                func_kwargs = config['kwargs'] if 'kwargs' in config else {}
                kwargs = {}
                for k, v in func_kwargs.items():
                    try:
                        kwargs.update({k: v[self._ftype]})
                    except TypeError:
                        kwargs.update({k: v})
                    if k in variable_kwargs:
                        kwargs.update({k: variable_kwargs[k]})
                value = config['func'](valid_arr, **kwargs)
                indcators_value_result.update({key: value})
                value_sorted = sorted(value, reverse=True)
                rank = [value_sorted.index(i) for i in value]
                indcators_rank_result.update({key: rank})

            indcators_value_result.update({'fund_id': valid_funds})
            indcators_rank_result.update({'fund_id': valid_funds})
            this_win_ind_value = DataFrame(indcators_value_result)
            this_win_ind_rank = DataFrame(indcators_rank_result)
            for ind_df in (this_win_ind_value, this_win_ind_rank):
                ind_df['freq'] = window
                ind_df['as_of_date_'] = self.cur_time
            ind_value_list.append(this_win_ind_value)
            ind_rank_list.append(this_win_ind_rank)

        if ind_value_list.__len__() > 0:
            final_value = concat(ind_value_list)
            final_value = final_value.merge(self.fund_info.loc[:, ['fund_id', 'S_INFO_WINDCODE']],
                                            on='fund_id', how='left')
            final_rank = concat(ind_rank_list)
            final_rank = final_rank.merge(self.fund_info.loc[:, ['fund_id', 'S_INFO_WINDCODE']],
                                          on='fund_id', how='left')
            return final_value, final_rank
        else:
            return None, None

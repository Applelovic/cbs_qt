from pandas import DataFrame, qcut, concat
from numpy import nan
from sqlalchemy import or_, and_, create_engine

from cbsqt.job.interface import AbstractJob

from .configs import RatingCategory, FwdFactorDict, BwdFactors, BaseColDic, AssetCol, StrategyCode
from .configs import StaticRiskRatingDict, InvsRiskFactorsDict, SupplementOrderDict, Splition, FactorIsolated
from .configs import ColumnNaming

from cbsqt.data.utils.engine import Engine
from cbsqt.data.utils.tool import QueryTool

from cbsqt.data.prod.cbaas import CBAASFund, Manager, ManagerFundHistory, FundCompany, CompanyFund
# from cbsqt.data.dev.quant import StaticRiskRatingMF, StaticRiskRatingHF


class ForwardRatingCal(AbstractJob):

    def __init__(self):
        self._cur_time = None
        self._date_str = None
        self._engine = Engine.lu_cbaas_test
        self._uploading_engine = create_engine('mysql+pymysql://cbaas:aNSQM88rSH@172.19.46.31:3306/cbaas?charset=utf8')

        self._prv_month = 0
        self._mf_monitor = 0
        self._hf_monitor = 0

        self._fwd_rating_holder = []
        self._bkwd_rating_holder = []
        self._rsk_rating_holder = []
        self._all_rating_holder = []
        self._history_rating_holder = []

        self._registered_rating_method = RatingCategory
        self._base_col_dict = BaseColDic
        self._strategy_code = StrategyCode
        self._asset_col = AssetCol
        self._cal_splitions = Splition
        self._fwd_factor_dict = FwdFactorDict
        self._bkd_factor_dict = BwdFactors
        self._static_risk_dict = StaticRiskRatingDict
        self._inv_risk_factor_dict = InvsRiskFactorsDict
        self._sup_reference_dict = SupplementOrderDict
        self._naming = ColumnNaming
        self._isolated = FactorIsolated

        print("Initialized.")

    def set_time(self, time_obj=None):
        if time_obj:
            self._cur_time = time_obj
            self._date_str = self._cur_time.date_.strftime('%Y-%m-%d')

    def run_singal(self):
        if ord(self._cur_time.is_week_end) == 1:
            cur_month = self._cur_time.date_.month
            if cur_month != self._prv_month:
                self._prv_month = cur_month
                return True

    def run_snapshot(self):
        # if self._cur_avail_hf_info.shape[0] >= 100:
        #     self.ratings_cal('fwd', 'HF')
        #     self.ratings_cal('bkwd', 'HF')
        #     self._hf_monitor = 1

        if self._cur_avail_mf_info.shape[0] >= 100:
            self.ratings_cal('fwd', 'MF')
            self.ratings_cal('bkwd', 'MF')
            self._mf_monitor = 1

        # print(self.fwd_rating_snapshot)
        # self.ratings_cal('bkwd', 'HF')
        # print(self._bkwd_rating_holder)
        # self.ratings_cal('rsk', 'MF')
        # self.ratings_cal('rsk', 'HF')
        # print(self._bkwd_rating_holder)

        if self._hf_monitor + self._mf_monitor > 0:
            self.snapshot_combine()
            self.uploading_all()
            print('{} uploaded.'.format(self.date))
        else:
            print('{} jumped.'.format(self.date))

        self.flush()

    def termination(self):
        print('All finished.')

    def flush(self):
        self._fwd_rating_holder = []
        self._bkwd_rating_holder = []
        self._rsk_rating_holder = []
        self._all_rating_holder = []
        self._mf_monitor = 0
        self._hf_monitor = 0

    @property
    def date(self):
        return self._date_str

    # @property
    # def _static_rsk_rating(self):
    #     rsk = QueryTool([])

    @property
    def _cur_avail_hf_info(self):
        info = QueryTool([CBAASFund.id.label('fund_id'),
                          CBAASFund.fund_name,
                          CBAASFund.strategy,
                          FundCompany.id.label('company_id'),
                          FundCompany.company_name],
                         self._engine). \
            join(CompanyFund).\
            join(FundCompany).\
            filter(CBAASFund.asset_class == 8).\
            filter(CBAASFund.inception_date <= self.date).\
            filter(CBAASFund.latest_nav_date >= self.date).all()

        return DataFrame(info)

    @property
    def _cur_avail_mf_info(self):
        info = QueryTool([CBAASFund.id.label('fund_id'),
                          CBAASFund.fund_name,
                          CBAASFund.strategy_category,
                          Manager.id.label('manager_id'),
                          Manager.first_name.label('manager_name'),
                          FundCompany.id.label('company_id'),
                          FundCompany.company_name],
                         self._engine). \
            join(ManagerFundHistory). \
            join(Manager). \
            join(FundCompany). \
            filter(CBAASFund.asset_class == 10). \
            filter(CBAASFund.inception_date <= self.date). \
            filter(CBAASFund.latest_nav_date >= self.date). \
            filter(or_(and_(ManagerFundHistory.start_date <= self.date,
                            ManagerFundHistory.end_date >= self.date),
                       and_(ManagerFundHistory.start_date <= self.date,
                            ManagerFundHistory.end_date.is_(None)))).all()
        return DataFrame(info)

    @property
    def avail_funds_info(self):
        return {'MF': self._cur_avail_mf_info, 'HF': self._cur_avail_hf_info}

    @property
    def rating_factor_dict(self):
        return {'bkwd': self._bkd_factor_dict,
                'fwd': self._fwd_factor_dict,
                'rsk': self._inv_risk_factor_dict}

    @property
    def rating_snapshot_holders(self):
        return {'bkwd': self._fwd_rating_holder,
                'fwd': self._bkwd_rating_holder,
                'rsk': self._rsk_rating_holder}

    @property
    def fwd_rating_snapshot(self):
        return concat(self._fwd_rating_holder)

    @property
    def bkwd_rating_snapshot(self):
        return concat(self._bkwd_rating_holder)

    @property
    def rsk_rating_snapshot(self):
        return concat(self._rsk_rating_holder)

    @property
    def all_rating_snapshot(self):
        return concat(self._all_rating_holder, axis=1).reset_index()

    def snapshot_combine(self):
        fwd = self.fwd_rating_snapshot.set_index(['fund_id', 'date'])
        self._all_rating_holder.append(fwd)

        bkwd = self.bkwd_rating_snapshot.set_index(['fund_id', 'date'])
        self._all_rating_holder.append(bkwd)

        # rsk = self.rsk_rating_snapshot.set_index(['fund_id', 'date'])
        # self._all_rating_holder.append(rsk)

    def uploading_all(self):
        # self.all_rating_snapshot.to_sql('fund_rating_copy1', self._uploading_engine, if_exists='append', index=False)
        pass

    def ratings_cal(self, rating_type='fwd', fund_type='MF'):

        if rating_type in self._registered_rating_method:
            factor_collection = self.rating_factor_dict[rating_type]
        else:
            raise ValueError('This is no rating type of {!r} prepared.'.format(rating_type))

        if fund_type not in ['MF', 'HF']:
            raise ValueError('Fund type should be either "MF" or "HF".')

        rating_params = {'rating_type': rating_type,
                         'fund_type': fund_type,
                         'fund_id_col': 'fund_id',
                         'date_col': 'date',
                         'names': self._naming[rating_type],
                         'strategy_col': self._asset_col[fund_type],
                         'funds_info': self.avail_funds_info[fund_type],
                         'factor_collection': factor_collection,
                         'base_col_dict': self._base_col_dict[fund_type],
                         'supplement_order': self._sup_reference_dict[fund_type],
                         'factor_isolated': self._isolated[rating_type],
                         'static_risk': self._static_risk_dict[fund_type],
                         'investing_risk': self._inv_risk_factor_dict[fund_type]}

        self.rating_method_guide(**rating_params)

    def rating_method_guide(self, rating_type, *args, **kwargs):
        if rating_type == 'fwd':
            self.fwd_rating_processing(*args, **kwargs)
        elif rating_type == 'bkwd':
            self.bkwd_rating_processing(*args, **kwargs)
        elif rating_type == 'rsk':
            self.rsk_rating_processing(*args, **kwargs)
        else:
            raise ValueError('Rating type {!r} is not registered.')

    def fwd_rating_processing(self, *args, **kwargs):
        if kwargs['funds_info'].shape[0] >= 100:
            self._fwd_rating_holder.append(self._strategy_diff(*args, **kwargs))

    def bkwd_rating_processing(self, *args, **kwargs):
        if kwargs['funds_info'].shape[0] >= 100:
            self._bkwd_rating_holder.append(self._strategy_diff(*args, **kwargs))

    def rsk_rating_processing(self, *args, **kwargs):
        print(kwargs['fund_type'])
        self._rsk_rating_holder.append(self._strategy_iden(*args, **kwargs))

    def _strategy_iden(self, fund_type, funds_info, factor_collection, factor_isolated=False, **kwargs):
        pass

    def _strategy_diff(self, fund_type, funds_info, strategy_col, factor_collection, factor_isolated=False, **kwargs):
        strategy_groups = funds_info.groupby(strategy_col)

        base_col_dict = kwargs['base_col_dict']
        rating_name = kwargs['names']['final']

        raw_ratings_list = []

        for strategy_key, df in strategy_groups:
            if strategy_key in self._strategy_code[fund_type]:
                strateg_name = self._strategy_code[fund_type][strategy_key]
            else:
                continue

            if strateg_name in factor_collection[fund_type]:
                factor_col = factor_collection[fund_type][strateg_name]
            else:
                factor_col = factor_collection[fund_type]
            strategy_funds = df['fund_id'].unique().tolist()

            if factor_isolated:
                indv_factor_rating_holder = []
                for factor_name, col in factor_col.items():
                    single_factor_cache = self._pure_rating_cal(funds=strategy_funds,
                                                                factor_col=[col],
                                                                base_col_dict=base_col_dict,
                                                                rating_name=factor_name)
                    indv_factor_rating_holder.append(single_factor_cache)
                raw_ratings_list.append(concat(indv_factor_rating_holder, axis=1))
                # rating_name = kwargs['names']['final']
            else:
                # rating_name = kwargs['names']['final']
                raw_ratings_list.append(self._pure_rating_cal(funds=strategy_funds,
                                                              factor_col=factor_col,
                                                              base_col_dict=base_col_dict,
                                                              rating_name=rating_name))
        raw_ratings = concat(raw_ratings_list)
        supplement_order = kwargs['supplement_order']
        rating_sup_label = kwargs['names']['sup']
        if factor_isolated:
            factor_filled_list = []
            factors = []
            for i in range(raw_ratings.shape[1]):
                filled_cache = self._supplementary_rating_cal(info=funds_info,
                                                              ratings=raw_ratings.iloc[:, i].to_frame(),
                                                              sup_list=supplement_order,
                                                              how='right')
                factor_filled_list.append(filled_cache)
                factors.append(raw_ratings.iloc[:, i].name)
            factor_filled = concat(factor_filled_list, axis=1)
            factor_filled[rating_name] = factor_filled.mean(axis=1).round()
            filled = self._supplementary_rating_cal(info=funds_info,
                                                    ratings=factor_filled[rating_name].to_frame(),
                                                    sup_list=supplement_order,
                                                    sup_label=rating_sup_label,
                                                    how='left')
            filled = filled.merge(factor_filled[factors], left_on='fund_id', right_index=True, how='left')
        else:
            filled = self._supplementary_rating_cal(info=funds_info,
                                                    ratings=raw_ratings,
                                                    sup_list=supplement_order,
                                                    sup_label=rating_sup_label,
                                                    how='left')

        date_col = kwargs['date_col']
        fund_id_col = kwargs['fund_id_col']
        needed_slices = [v for k, v in kwargs['names'].items()]
        needed_slices.append(fund_id_col)
        needed_slices.append(date_col)

        filled[date_col] = self.date
        final_rating = filled[needed_slices]
        return final_rating

    def _pure_rating_cal(self, funds, base_col_dict, factor_col, rating_name):
        cols = factor_col
        cols.append(base_col_dict['fund_id'])

        query_list = QueryTool(cols, self._engine).\
            filter(base_col_dict['fund_id'].in_(funds)).\
            filter(base_col_dict['date'] == self.date).\
            all()

        if len(query_list) > 0:
            factor_value = DataFrame(query_list).set_index('fund_id').dropna()
            standardized = self._clean_and_standarize(factor_value)
            raw_rating = self._rating_cal(standardized.mean(axis=1),
                                          qcut,
                                          [0., .1, .325, .675, .9, 1.],
                                          labels=False,
                                          duplicates='drop')
            return raw_rating.to_frame(rating_name)
        else:
            return DataFrame(columns=[rating_name])

    @staticmethod
    def _clean_and_standarize(df, clip_rate=0.05, clip_side='double'):

        def slice_clean(ser, rate, side):
            if side == 'double':
                ser[ser >= ser.quantile(1-rate)] = nan
                ser[ser <= ser.quantile(rate)] = nan
            elif side == 'left':
                ser[ser <= ser.quantile(rate)] = nan
            elif side == 'right':
                ser[ser >= ser.quantile(1 - rate)] = nan
            else:
                raise NotImplementedError
            return ser

        cleaned = df.apply(slice_clean, rate=clip_rate, side=clip_side).dropna()
        standardized = cleaned.apply(lambda ser: (ser - ser.min())/(ser.max() - ser.min()), axis=0)
        return standardized

    @staticmethod
    def _rating_cal(score_series, func, *args, **kwargs):
        return func(score_series, *args, **kwargs)

    def _supplementary_rating_cal(self, info, ratings, sup_list=None, sup_label=None, how='left'):
        info_with_rating = info.merge(ratings, left_on='fund_id', right_index=True, how=how)

        if sup_label:
            info_with_rating[sup_label] = info_with_rating[ratings.columns].isnull().astype(int)

        if not sup_list:
            return info_with_rating
        info_with_rating.set_index('fund_id', inplace=True)
        for cur_sup_col in sup_list:
            cache_supplemented_ratings = info_with_rating.groupby(cur_sup_col).\
                apply(self._element_sup, ref_col=cur_sup_col, rating_cal=ratings.columns[0]).\
                reset_index(level=0).\
                drop(cur_sup_col, axis=1)
            if cache_supplemented_ratings.shape[0] > 0:
                info_with_rating[ratings.columns] = info_with_rating[ratings.columns].\
                    fillna(cache_supplemented_ratings.iloc[:, 0])

        cleaned = info_with_rating.reset_index().\
            sort_values(['fund_id', ratings.columns[0]]).\
            drop_duplicates(['fund_id'], keep='last')
        if sup_label:
            return cleaned
        else:
            return cleaned.set_index('fund_id')[ratings.columns]

    @staticmethod
    def _element_sup(df, ref_col, rating_cal):
        if isinstance(ref_col, str) or isinstance(ref_col, int):
            representitive = int(round(df[rating_cal].mean())) if df[rating_cal].dropna().shape[0] > 0 else nan
            return df[rating_cal].fillna(representitive)
        else:
            return df[rating_cal]

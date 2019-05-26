from abc import ABCMeta, abstractmethod


class AbstractManagerReport(metaclass=ABCMeta):

    @abstractmethod
    def summary(self):
        raise NotImplementedError

    @abstractmethod
    def investing_rating(self):
        raise NotImplementedError

    @abstractmethod
    def risk_management_rating(self):
        raise NotImplementedError

    @abstractmethod
    def under_management_funds(self):
        raise NotImplementedError


class AbstractFundSummary(metaclass=ABCMeta):

    @abstractmethod
    def fund_name(self):
        raise NotImplementedError

    @abstractmethod
    def fund_current_aum(self):
        raise NotImplementedError

    @abstractmethod
    def fund_nav(self):
        raise NotImplementedError

    @abstractmethod
    def benchmark_nav(self):
        raise NotImplementedError

    @abstractmethod
    def fund_stats(self):
        raise NotImplementedError

    @abstractmethod
    def labels(self):
        raise NotImplementedError

    @abstractmethod
    def top_holding_tickers(self):
        raise NotImplementedError


class AbstractStats(metaclass=ABCMeta):

    @abstractmethod
    def start_date(self):
        raise NotImplementedError

    @abstractmethod
    def end_date(self):
        raise NotImplementedError

    @abstractmethod
    def cumulative_return(self):
        raise NotImplementedError

    @abstractmethod
    def annulized_return(self):
        raise NotImplementedError

    @abstractmethod
    def max_drawdown(self):
        raise NotImplementedError

    @abstractmethod
    def sharpe_ratio(self):
        raise NotImplementedError

    @abstractmethod
    def sortino_ratio(self):
        raise NotImplementedError

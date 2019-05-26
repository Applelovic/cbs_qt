from cbsqt.data.utils.tool import Base
from sqlalchemy import String, Column, Float, Integer, Date


class InvestingRiskThresholds(Base):

    __tablename__ = 'beta_investing_risk_thresholds'
    __table_args__ = {'schema': 'cbaas_quant'}
    key = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, index=True)
    fund_type = Column(String(10), index=True)
    MDD = Column(Float(6))
    Vol = Column(Float(6))
    CVaR = Column(Float(6))
    TailRisk = Column(Float(6))


class FundRating(Base):

    __tablename__ = 'alpha_fund_rating'
    __table_args__ = {'schema': 'cbaas_quant'}
    key = Column(Integer, primary_key=True, autoincrement=True)
    fund_id = Column(Integer, index=True)
    date = Column(Integer, index=True)
    mdd_rating = Column(Float(6))
    vol_rating = Column(Float(6))
    cvar_rating = Column(Float(6))
    tailrisk_rating = Column(Float(6))

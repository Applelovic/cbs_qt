from cbsqt.data.utils.tool import Base
from sqlalchemy import String, Column, Integer


class StaticRiskRatingHF(Base):

    __tablename__ = 'beta_static_risk_rating_hf'
    __table_args__ = {'schema': 'quant'}
    fund_id = Column(Integer, primary_key=True)
    fund_name = Column(String(100))
    org_name = Column(String(100))
    liquidity = Column(Integer)
    credit = Column(Integer)
    operational = Column(Integer)
    regulatory = Column(Integer)


class StaticRiskRatingMF(Base):

    __tablename__ = 'beta_static_risk_rating_mf'
    __table_args__ = {'schema': 'quant'}
    fund_id = Column(Integer, primary_key=True)
    strategy = Column(String(10))
    liquidity = Column(Integer)
    credit = Column(Integer)
    operational = Column(Integer)
    regulatory = Column(Integer)


if __name__ == '__main__':
    from cbaasquant.data.utils.tool import QueryTool
    from cbaasquant.data.utils.engine import Engine
    from pandas import DataFrame

    engine = Engine.lu_cbaas_dev
    test = QueryTool([StaticRiskRatingMF.fund_id,
                      (-1*StaticRiskRatingMF.liquidity).label('liquidity'),
                      StaticRiskRatingMF.credit],
                     engine)[:5]
    print(DataFrame(test))

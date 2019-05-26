from sqlalchemy import String, Column, Float  # Integer

from cbsqt.data.utils.tool import Base


class ChinaMutualFundNAV(Base):

    __tablename__ = 'chinamutualfundnav'
    __table_args__ = {'schema': 'wind_from_lu_oracle'}
    OBJECT_ID = Column(String(100), primary_key=True)
    F_INFO_WINDCODE = Column(String(40), index=True)
    PRICE_DATE = Column(String(8), index=True)
    F_NAV_ADJUSTED = Column(Float(4))
    F_NAV_UNIT = Column(Float(4))
    F_NAV_ACCUMULATED = Column(Float(4))
    F_NAV_ADJFACTOR = Column(Float(4))
    F_PRT_NETASSET = Column(Float(4))
    NETASSET_TOTAL = Column(Float(4))


class AIndexEODPrices(Base):

    __tablename__ = 'AINDEXEODPRICES'
    __table_args__ = {'schema': 'wind_from_lu_oracle'}
    OBJECT_ID = Column(String(100), primary_key=True)
    S_INFO_WINDCODE = Column(String(40), index=True)
    TRADE_DT = Column(String(8))
    S_DQ_PRECLOSE = Column(Float(4))
    S_DQ_OPEN = Column(Float(4))
    S_DQ_HIGH = Column(Float(4))
    S_DQ_LOW = Column(Float(4))
    S_DQ_CLOSE = Column(Float(4))
    S_DQ_CHANGE = Column(Float(4))
    S_DQ_PCTCHANGE = Column(Float(4))
    S_DQ_VOLUME = Column(Float(4))
    S_DQ_AMOUNT = Column(Float(4))


class CBondEODPrices(Base):

    __tablename__ = 'cbindexeodprices'
    __table_args__ = {'schema': 'wind_from_lu_oracle'}
    OBJECT_ID = Column(String(100), primary_key=True)
    S_INFO_WINDCODE = Column(String(40), index=True)
    TRADE_DT = Column(String(8))
    S_DQ_PRECLOSE = Column(Float(4))
    S_DQ_OPEN = Column(Float(4))
    S_DQ_HIGH = Column(Float(4))
    S_DQ_LOW = Column(Float(4))
    S_DQ_CLOSE = Column(Float(4))
    S_DQ_CHANGE = Column(Float(4))
    S_DQ_PCTCHANGE = Column(Float(4))
    S_DQ_VOLUME = Column(Float(4))
    S_DQ_AMOUNT = Column(Float(4))
    S_DQ_AVGPRICE = Column(Float(4))
    S_DQ_TRADESTATUS = Column(String(10))


class AShareEODPrices(Base):

    __tablename__ = 'ashareeodprices'
    __table_args__ = {'schema': 'wind_from_lu_oracle'}
    OBJECT_ID = Column(String(100), primary_key=True)
    S_INFO_WINDCODE = Column(String(40), index=True)
    TRADE_DT = Column(String(8))
    S_DQ_PRECLOSE = Column(Float(4))
    S_DQ_OPEN = Column(Float(4))
    S_DQ_HIGH = Column(Float(4))
    S_DQ_LOW = Column(Float(4))
    S_DQ_CLOSE = Column(Float(4))
    S_DQ_CHANGE = Column(Float(4))
    S_DQ_PCTCHANGE = Column(Float(4))
    S_DQ_VOLUME = Column(Float(4))
    S_DQ_AMOUNT = Column(Float(4))
    S_DQ_ADJPRECLOSE = Column(Float(4))
    S_DQ_ADJOPEN = Column(Float(4))
    S_DQ_ADJHIGH = Column(String(10))
    S_DQ_ADJLOW = Column(String(10))
    S_DQ_ADJCLOSE = Column(String(10))
    S_DQ_ADJFACTOR = Column(String(10))
    S_DQ_AVGPRICE = Column(String(10))
    S_DQ_TRADESTATUS = Column(String(10))


if __name__ == '__main__':

    # test
    from cbaasquant.data.utils.engine import Engine
    from cbaasquant.data.utils.tool import QueryTool
    from pandas import DataFrame

    engine = Engine.lu_cbaas_dev
    # Base.matadata.reflect(engine, schema='wind_from_lu_oracle')
    test = QueryTool([ChinaMutualFundNAV.F_INFO_WINDCODE,
                      ChinaMutualFundNAV.PRICE_DATE,
                      ChinaMutualFundNAV.F_NAV_ADJUSTED], engine).\
        filter(ChinaMutualFundNAV.F_INFO_WINDCODE == '184688.SZ').all()
    print(DataFrame(test))

from cbsqt.data.prod.cbaas_quant import InvestingRiskThresholds, FundRating
from cbsqt.data.utils.tool import Base
from cbsqt.data.utils.engine import Engine

if __name__ == '__main__':
    Base.metadata.create_all(Engine('cbaas_quant').lu_cbaas_test)

from cbsqt.job.risk_rating import InvestingRiskHF
from cbsqt.main import run

if __name__ == '__main__':
    run('2018-01-01', '2018-01-31', [InvestingRiskHF()])

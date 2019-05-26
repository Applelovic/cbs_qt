from cbsqt.job.cbaas_rating.rating import ForwardRatingCal
from cbsqt.main import run


if __name__ == '__main__':
    run('2012-01-01', '2012-06-31', [ForwardRatingCal()])

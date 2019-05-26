from cbsqt.config import TimeAxis
from cbsqt.job import JobBook
# from multiprocessing import Pool


def run(start, end, jobs=JobBook):
    # multi = Pool()
    times = TimeAxis(start, end)
    for time_tick in times.elements:
        for job in jobs:
            job.set_time(time_tick)
            if job.run_singal():
                # multi.apply_async(job.run_snapshot())
                job.run_snapshot()

    # multi.close()
    # multi.join()

    for job in jobs:
        job.termination()


if __name__ == '__main__':
    run('2018-01-01', '2018-01-31')

"""
Telecom Systems Development Kit - tsdk
"""

import json as _json
import sys as _sys
from datetime import datetime as _datetime
from pathlib import Path as _Path

from apscheduler.events import EVENT_ALL as _EVENT_ALL
from apscheduler.executors.pool import ProcessPoolExecutor as _ProcessPoolExecutor
from apscheduler.executors.pool import ThreadPoolExecutor as _ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore as _MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler as _BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler as _BlockingScheduler
from dateutil import tz as _tz

from tsdk.common.logs import ErrorLog as _Error_log
from tsdk.common.logs import SchedulerLog as _SchedulerLog
from tsdk.common.tsdk_server import SchedulerSchemaParams as _Ssp
from tsdk.common.tsdk_server import SystemSchemas as _Ss
from tsdk.common.tsdk_server import TsdkServer as _Tsdk

__all__ = ['TsdkScheduler']

job_stores = {
    'default': _MemoryJobStore()
}
executors = {
    'default': _ThreadPoolExecutor(max_workers=60),
    'processpool': _ProcessPoolExecutor(max_workers=60)
}
job_defaults = {
    'coalesce': True,
    'max_instances': 1
}


def _listener(event):
    if hasattr(event, 'job_id'):
        if event.job_id != 'scheduler_job':
            _SchedulerLog.write('job event jobid: %s, event: %s' %
                                (event.job_id,
                                 event.exception if hasattr(event, 'exception') else ''))


def _toUTC(time_string):
    try:
        utc_zone = _tz.tzutc()
        local_zone = _tz.tzlocal()
        fmt = '%Y-%m-%d %H:%M:%S'
        local_time = _datetime.strptime(time_string, fmt)
        local_time = local_time.replace(tzinfo=local_zone)
        utc_time = local_time.astimezone(utc_zone)
        return utc_time.strftime(fmt)
    except Exception as e:
        _Error_log.write(e)
        return ''


def _validate_time(date_text):
    try:
        fmt = '%Y-%m-%d %H:%M:%S'
        _datetime.strptime(date_text, fmt)
        return True
    except ValueError:
        # print('Incorrect date format')
        return False


class TsdkScheduler(object):
    def __init__(self, scheduler_type='Blocking', jobs_df=None):
        self.type = scheduler_type
        self.job_interval = 1
        self.jobs = jobs_df
        if self.type == 'Blocking':
            self.scheduler = _BlockingScheduler(jobstores=job_stores,
                                                executors=executors,
                                                job_defaults=job_defaults)
        else:
            self.scheduler = _BackgroundScheduler(jobstores=job_stores,
                                                  executors=executors,
                                                  job_defaults=job_defaults)

    def shutdown(self):
        self.scheduler.shutdown(wait=False)

    def pause(self):
        self.scheduler.pause()

    def resume(self):
        self.scheduler.resume()

    def start(self, paused=False):
        self.scheduler.add_listener(_listener, _EVENT_ALL)
        self.scheduler.add_job(self.scheduler_job, 'interval',
                               seconds=self.job_interval, id='scheduler_job')
        self.scheduler.start(paused)

    def scheduler_job(self):
        if self.jobs is None:
            tsdk = _Tsdk()
            df, err = tsdk.sql_to_dataframe(
                "SELECT * FROM " + _Ss.Scheduler)
            df.columns = map(str.lower, df.columns)
            df = df.astype(str).apply(lambda x: x.str.lower())
        else:
            df = self.jobs
        # for job in self.scheduler.get_jobs():
        #    print("name: %s, trigger: %s, next run: %s, id: %s" % (
        #        job.name, job.trigger, job.next_run_time, job.id))
        for index, row in df.iterrows():
            if row[_Ssp.Enabled]:
                if row[_Ssp.ScheduleType] == 'date':
                    if self.scheduler.get_job(row[_Ssp.ID]) is None:
                        try:
                            _sys.path.append(str(_Path(row[_Ssp.Module]).parent))
                            func = getattr(__import__(_Path(row[_Ssp.Module]).stem), row[_Ssp.Function])
                            kwargs = _json.loads(row[_Ssp.Argument].replace("'", "\"")) if len(
                                row[_Ssp.Argument]) > 0 else ''
                            self.scheduler.add_job(func, 'date',
                                                   kwargs=kwargs,
                                                   run_date=row[_Ssp.RunTime],
                                                   id=row[_Ssp.ID])
                            # print('job added %s', {row[_Ssp.ID]})
                            _SchedulerLog.write('job added %s' % row[_Ssp.ID])
                        except Exception as e:
                            _Error_log.write(e)
                elif row[_Ssp.ScheduleType] == "interval":
                    if self.scheduler.get_job(row[_Ssp.ID]) is None:
                        try:
                            _sys.path.append(str(_Path(row[_Ssp.Module]).parent))
                            func = getattr(__import__(_Path(row[_Ssp.Module]).stem), row[_Ssp.Function])
                            kwargs = _json.loads(row[_Ssp.Argument].replace("'", "\"")) if len(
                                row[_Ssp.Argument]) > 0 else ''
                            self.scheduler.add_job(func, 'interval',
                                                   kwargs=kwargs,
                                                   minutes=row[_Ssp.Periodicity],
                                                   start_date=row[_Ssp.StartTime],
                                                   end_date=row[_Ssp.EndTime],
                                                   id=row[_Ssp.ID])
                            # print('job added %s', {row[_Ssp.ID]})
                            _SchedulerLog.write('job added %s' % row[_Ssp.ID])
                        except Exception as e:
                            _Error_log.write(e)
                else:
                    pass


if __name__ == '__main__':
    import pandas as pd

    jobs = {'algorithm': ['test1', 'test2'],
            'enabled': [True, True],
            'schedule_type': ['date', 'interval'],
            'periodicity': [1440, 1440],
            'runtime': ['2023-05-17 00:00:00', ''],
            'start_time': ['', '2022-05-18 00:00:00'],
            'end_time': ['', '2023-05-17 00:00:00'],
            'module': ['c:/users/ali/desktop/test_desktop', 'c:/users/ali/desktop/test_desktop2'],
            'function': ['testx', 'testx2'],
            'argument': ['{}', ''],
            'category': ['test', 'test'],
            'developer': ['test', 'test'],
            'id': ['job1', 'job2']}

    sch = TsdkScheduler(jobs_df=pd.DataFrame.from_dict(jobs))
    sch.start()

import pandas as _pd

from tsdk.common.tsdk_server import LogicsLogSchema as _LogicsLogSchema
from tsdk.common.tsdk_server import LogsSchema as _LogsSchema
from tsdk.common.tsdk_server import SystemSchemas as _SystemSchemas
from tsdk.common.tsdk_server import TsdkServer as _Tsdk

__all__ = ['DBLogs', 'DBLogicsLogs']


class DBLogs(object):
    def __init__(self,
                 logicname,
                 periodicity,
                 category,
                 printerrors,
                 developer):
        self._logicname = logicname
        self._periodicity = periodicity
        self._category = category
        self._printerrors = printerrors
        self._developer = developer

    def write(self, msg):
        df = _pd.DataFrame(_LogsSchema)
        df.iloc[0] = [self._logicname,
                      self._periodicity,
                      self._category,
                      self._printerrors,
                      self._developer,
                      msg,
                      _pd.Timestamp.now(),
                      _pd.to_datetime(_pd.Timestamp.now()).date()]
        return _Tsdk().dataframe_to_db(df, _SystemSchemas.Logs)


class DBLogicsLogs(object):
    def __init__(self):
        pass

    def write(self, logicname, family, database, layertechnology, mokey, parameter, oldvalue, newvalue, time, date):
        df = _pd.DataFrame(_LogicsLogSchema)
        df.iloc[0] = [logicname,
                      family,
                      database,
                      layertechnology,
                      mokey,
                      parameter,
                      oldvalue,
                      newvalue,
                      _pd.Timestamp.now(),
                      _pd.to_datetime(_pd.Timestamp.now()).date()]
        return _Tsdk().dataframe_to_db(df, _SystemSchemas.LogicsLogs)

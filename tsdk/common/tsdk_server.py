"""
Telecom Systems Development Kit - tsdk
"""

import json as _json

import pandas as _pd
from strenum import StrEnum as _StrEnum

import tsdk.common.dbconfig as _dbconfig
from tsdk.common.dbconfig import DbConfig as _DbConfig
from tsdk.common.dbconfig import OdbcDrivers as _OdbcDrivers
from tsdk.common.dbmanager import SQLServer as _SQLServer

__all__ = [
    'SystemSchemas',
    'LogicsSchemaParams',
    'SchedulerSchemaParams',
    'LogsSchemaParams',
    'LogicsLogSchemaParams',
    'ExcludeNEsParams',
    'LogicsSchema',
    'SchedulerSchema',
    'LogsSchema',
    'LogicsLogSchema',
    'ExcludeNEsSchema',
    'Logics',
    'TsdkServer']


class _Conf(object):
    Driver = _OdbcDrivers.MicrosoftSQLServer
    Server = "desktop-v8venfm"
    Database = "tsdk"
    Uid = ""
    Pwd = ""
    Trusted = True


class SystemSchemas(_StrEnum):
    Logics = "logics",
    Scheduler = "scheduler",
    Logs = "logs",
    LogicsLogs = "logics_logs",
    ExcludeNEs = "exclude_nes"


class ExcludeNEsParams(_StrEnum):
    MOKey = "mo_key"


class LogicsSchemaParams(_StrEnum):
    LogicName = "logic_name",
    Family = "family",
    Database = "database",
    LayerTechnology = "layer_technology",
    MOKey = "mo_key",
    Parameter = "parameter",
    ParameterValue = "parameter_value",
    ExcludedNEs = "excluded_nes",
    Enabled = "enabled",
    FreeSQL = "freesql",


class SchedulerSchemaParams(_StrEnum):
    Algorithm = "algorithm",
    Enabled = "enabled",
    ScheduleType = "schedule_type",
    Periodicity = "periodicity",
    RunTime = "runtime",
    StartTime = "start_time",
    EndTime = "end_time",
    Module = "module",
    Function = "function",
    Argument = "argument",
    Category = "category",
    Developer = "developer",
    ID = "id"


class LogsSchemaParams(_StrEnum):
    LogicName = "logic_name",
    Periodicity = "periodicity",
    Category = "category",
    PrintErrors = "print_errors",
    Developer = "developer",
    Msg = "msg",
    Time = "time",
    Date = "date",


class LogicsLogSchemaParams(_StrEnum):
    LogicName = "logic_name",
    Family = "family",
    Database = "database",
    LayerTechnology = "layer_technology",
    MOKey = "mo_key",
    Parameter = "parameter",
    OldValue = "old_value",
    NewValue = "new_value",
    Time = "time",
    Date = "date",


ExcludeNEsSchema = {
    ExcludeNEsParams.MOKey: _pd.Series(dtype='str')
}

LogicsSchema = {
    LogicsSchemaParams.LogicName: _pd.Series(dtype='str'),
    LogicsSchemaParams.Family: _pd.Series(dtype='str'),
    LogicsSchemaParams.Database: _pd.Series(dtype='str'),
    LogicsSchemaParams.LayerTechnology: _pd.Series(dtype='str'),
    LogicsSchemaParams.MOKey: _pd.Series(dtype='str'),
    LogicsSchemaParams.Parameter: _pd.Series(dtype='str'),
    LogicsSchemaParams.ParameterValue: _pd.Series(dtype='str'),
    LogicsSchemaParams.ExcludedNEs: _pd.Series(dtype='str'),
    LogicsSchemaParams.Enabled: _pd.Series(dtype='bool'),
    LogicsSchemaParams.FreeSQL: _pd.Series(dtype='str')
}

SchedulerSchema = {
    SchedulerSchemaParams.Algorithm: _pd.Series(dtype='str'),
    SchedulerSchemaParams.Enabled: _pd.Series(dtype='bool'),
    SchedulerSchemaParams.Periodicity: _pd.Series(dtype='int'),
    SchedulerSchemaParams.RunTime: _pd.Series(dtype='str'),
    SchedulerSchemaParams.StartTime: _pd.Series(dtype='str'),
    SchedulerSchemaParams.EndTime: _pd.Series(dtype='str'),
    SchedulerSchemaParams.Module: _pd.Series(dtype='str'),
    SchedulerSchemaParams.Function: _pd.Series(dtype='str'),
    SchedulerSchemaParams.Argument: _pd.Series(dtype='str'),
    SchedulerSchemaParams.Category: _pd.Series(dtype='str'),
    SchedulerSchemaParams.Developer: _pd.Series(dtype='str'),
    SchedulerSchemaParams.ID: _pd.Series(dtype='str')
}

LogsSchema = {
    LogsSchemaParams.LogicName: _pd.Series(dtype='str'),
    LogsSchemaParams.Periodicity: _pd.Series(dtype='int'),
    LogsSchemaParams.Category: _pd.Series(dtype='str'),
    LogsSchemaParams.PrintErrors: _pd.Series(dtype='str'),
    LogsSchemaParams.Developer: _pd.Series(dtype='str'),
    LogsSchemaParams.Msg: _pd.Series(dtype='str'),
    LogsSchemaParams.Time: _pd.Series(dtype='str'),
    LogsSchemaParams.Date: _pd.Series(dtype='str')
}

LogicsLogSchema = {
    LogicsLogSchemaParams.LogicName: _pd.Series(dtype='str'),
    LogicsLogSchemaParams.Family: _pd.Series(dtype='str'),
    LogicsLogSchemaParams.Database: _pd.Series(dtype='str'),
    LogicsLogSchemaParams.LayerTechnology: _pd.Series(dtype='str'),
    LogicsLogSchemaParams.MOKey: _pd.Series(dtype='str'),
    LogicsLogSchemaParams.Parameter: _pd.Series(dtype='str'),
    LogicsLogSchemaParams.OldValue: _pd.Series(dtype='str'),
    LogicsLogSchemaParams.NewValue: _pd.Series(dtype='str'),
    LogicsLogSchemaParams.Time: _pd.Series(dtype='str'),
    LogicsLogSchemaParams.Date: _pd.Series(dtype='str')
}


class Logics(_StrEnum):
    NR_Basic_Audit_V2 = "nr_basic_audit_v2"


class TsdkServer(_SQLServer):
    def __init__(self,
                 dbconfig: _DbConfig = _DbConfig(_Conf.Driver,
                                                 _Conf.Server,
                                                 _Conf.Database,
                                                 _Conf.Uid,
                                                 _Conf.Pwd,
                                                 _Conf.Trusted)) -> None:
        super().__init__(dbconfig)
        self.conf = 'conf.json'
        self.dbconfig = self.ConnectionString.dbconfig

    def set_configuration(self, Driver, Server, Database, Uid, Pwd, Trusted):
        super().__init__(_DbConfig(_dbconfig.get_odbc_driver(Driver),
                                   Server,
                                   Database,
                                   Uid,
                                   Pwd,
                                   Trusted))

    def load_configuration(self, conf: str = ''):
        if not conf:
            conf = self.conf
        with open(conf, 'rb') as f:
            conf_json = _json.load(f)
            super().__init__(_DbConfig(_dbconfig.get_odbc_driver(conf_json['DRIVER']),
                                       conf_json['SERVER'],
                                       conf_json['DATABASE'],
                                       conf_json['UID'],
                                       conf_json['PWD'],
                                       conf_json['TRUSTED']))

    def save_configuration(self, conf: str = ''):
        conf_json = {
            'DRIVER': _dbconfig.get_odbc_driver_str(self.dbconfig.server),
            'SERVER': self.dbconfig.server,
            'DATABASE': self.dbconfig.database,
            'UID': self.dbconfig.uid,
            'PWD': self.dbconfig.pwd,
            'TRUSTED': self.dbconfig.trusted,
        }
        if not conf:
            conf = self.conf
        with open(conf, 'w') as f:
            _json.dump(conf_json, f, indent=4)

    def setup_database(self):
        db = 'tsdk'
        if self.dbconfig.database != 'tsdk':
            db = self.dbconfig.database
            self.dbconfig.database = 'tsdk'

        self.execute_sql("DROP TABLE IF EXISTS " + SystemSchemas.Logics)
        df = _pd.DataFrame(LogicsSchema)
        self.dataframe_to_db(df, SystemSchemas.Logics)

        self.execute_sql("DROP TABLE IF EXISTS " + SystemSchemas.Scheduler)
        df = _pd.DataFrame(SchedulerSchema)
        self.dataframe_to_db(df, SystemSchemas.Scheduler)

        self.execute_sql("DROP TABLE IF EXISTS " + SystemSchemas.Logs)
        df = _pd.DataFrame(LogsSchema)
        self.dataframe_to_db(df, SystemSchemas.Logs)

        self.execute_sql("DROP TABLE IF EXISTS " + SystemSchemas.LogicsLogs)
        df = _pd.DataFrame(LogicsLogSchema)
        self.dataframe_to_db(df, SystemSchemas.LogicsLogs)

        self.execute_sql("DROP TABLE IF EXISTS " + SystemSchemas.ExcludeNEs)
        df = _pd.DataFrame(ExcludeNEsSchema)
        self.dataframe_to_db(df, SystemSchemas.ExcludeNEs)

        self.dbconfig.database = db

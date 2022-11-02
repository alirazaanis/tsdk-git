"""
Telecom Systems Development Kit - tsdk
"""

import logging
from os.path import dirname, abspath

from tsdk.common import *
from tsdk.logics import *

__all__ = [
    'SshConfig',  # sshconfig.py
    'DbConfig', 'OdbcDrivers', 'ConnectionString',  # dbconfig.py
    'SQLServer',  # dbmanager.py
    'copy_data',  # dbtasks.py
    'SystemSchemas', 'ExcludeNEsParams', 'ExcludeNEsSchema',  # tsdk_server.py
    'LogicsSchemaParams', 'SchedulerSchemaParams', 'LogsSchemaParams', 'LogicsLogSchemaParams',  # tsdk_server.py
    'LogicsSchema', 'SchedulerSchema', 'LogsSchema', 'LogicsLogSchema',  # tsdk_server.py
    'Logics', 'TsdkServer',  # tsdk_server.py
    'ErrorLog', 'QueryLog', 'SchedulerLog', 'Log', 'AllLog',  # logs.py
    'DBLogs', 'DBLogicsLogs',  # dblogs.py
    'TsdkScheduler',  # tsdk_scheduler.py
    'nr_basic_audit_v2'
]

ROOT_DIR = dirname(abspath(__file__))

handler = logging.FileHandler('tsdk_error.log', 'a')
handler.setFormatter(logging.Formatter('%(asctime)s @ %(levelname)s @ %(funcName)s @ %(message)s'))
log = logging.getLogger('ErrorLog')
log.setLevel(logging.ERROR)
log.addHandler(handler)

handler = logging.FileHandler('tsdk_query.log', 'a')
handler.setFormatter(logging.Formatter('%(asctime)s @ %(funcName)s @ %(message)s'))
log = logging.getLogger('QueryLog')
log.setLevel(logging.ERROR)
log.addHandler(handler)

handler = logging.FileHandler('tsdk_log.log', 'a')
handler.setFormatter(logging.Formatter('%(asctime)s @ %(funcName)s @ %(message)s'))
log = logging.getLogger('Log')
log.setLevel(logging.ERROR)
log.addHandler(handler)

handler = logging.FileHandler('tsdk_all.log', 'a')
handler.setFormatter(logging.Formatter('%(asctime)s @ %(funcName)s @ %(message)s'))
log = logging.getLogger('AllLog')
log.setLevel(logging.ERROR)
log.addHandler(handler)

handler = logging.FileHandler('tsdk_scheduler.log', 'a')
handler.setFormatter(logging.Formatter('%(asctime)s @ %(funcName)s @ %(message)s'))
log = logging.getLogger('apscheduler')
log.setLevel(logging.ERROR)
log.addHandler(handler)

del handler, log, logging, dirname, abspath

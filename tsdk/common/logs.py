import logging as _logging

__all__ = ['ErrorLog', 'QueryLog', 'SchedulerLog', 'Log', 'AllLog']


class ErrorLog(object):
    @staticmethod
    def write(msg):
        _logging.getLogger('ErrorLog').error(msg)


class QueryLog(object):
    @staticmethod
    def write(msg):
        _logging.getLogger('QueryLog').error(msg)


class SchedulerLog(object):
    @staticmethod
    def write(msg):
        _logging.getLogger('apscheduler').error(msg)


class Log(object):
    @staticmethod
    def write(msg):
        _logging.getLogger('Log').error(msg)


class AllLog(object):
    @staticmethod
    def write(msg):
        _logging.getLogger('AllLog').error(msg)

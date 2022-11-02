"""
Telecom Systems Development Kit - tsdk
"""

import sqlite3 as _sqlite3

import pandas as _pd
import pyodbc as _po
from sqlalchemy import create_engine as _create_engine

from tsdk.common.dbconfig import ConnectionString as _ConnectionString
from tsdk.common.dbconfig import DbConfig as _DbConfig
from tsdk.common.dbconfig import OdbcDrivers as _OdbcDrivers
from tsdk.common.logs import ErrorLog as _Error_log
from tsdk.common.logs import QueryLog as _Query_log

__all__ = ['SQLServer']


class SQLServer(object):

    def __init__(self, dbconfig: _DbConfig):
        self._connectionString: \
            _ConnectionString = _ConnectionString(dbconfig)
        self._connection = None
        self._engine = None
        self.Cursor = None

    @property
    def Engine(self):
        self._engine = \
            _create_engine(self._connectionString.get_url, fast_executemany=True)
        return self._engine

    @property
    def Connection(self):
        if self._connectionString.dbconfig.driver == _OdbcDrivers.SQLite:
            self._connection = \
                _sqlite3.connect(self._connectionString.dbconfig.database)
        else:
            self._connection = _po.connect(self._connectionString.get_odbc)
        return self._connection

    @property
    def ConnectionString(self):
        return self._connectionString

    def sql_to_dataframe(self, sql: str) -> (_pd.DataFrame, Exception):
        _Query_log.write(sql)
        df = _pd.DataFrame()
        err = None
        try:
            if self._connectionString.dbconfig.driver == _OdbcDrivers.SQLite:
                self._connection = \
                    _sqlite3.connect(self._connectionString.dbconfig.database)
            else:
                self._connection = _po.connect(self._connectionString.get_odbc)
            df = _pd.read_sql(sql, con=self._connection)
            self._connection.close()
        except Exception as e:
            _Error_log.write(e)
            err = e
        return df, err

    def sql_to_dataframe_2(self, sql: str) -> (_pd.DataFrame, Exception):
        _Query_log.write(sql)
        err = None
        df = _pd.DataFrame()
        try:
            if self._connectionString.dbconfig.driver == _OdbcDrivers.SQLite:
                self._connection = \
                    _sqlite3.connect(self._connectionString.dbconfig.database)
            else:
                self._connection = _po.connect(self._connectionString.get_odbc)
            self.Cursor = self._connection.cursor()
            self.Cursor.execute(sql)
            df = _pd.DataFrame([list(row) for row in self.Cursor],
                               columns=[column[0] for column in self.Cursor.description])
            self.Cursor.close()
            self._connection.close()
        except Exception as e:
            _Error_log.write(e)
            err = e
        return df, err

    def dataframe_to_db(self,
                        df: _pd.DataFrame,
                        table_name: str,
                        if_exists='append',
                        index=False) -> Exception:
        err = None
        try:
            self._engine = \
                _create_engine(self._connectionString.get_url, fast_executemany=True)
            df.to_sql(table_name,
                      con=self._engine,
                      if_exists=if_exists,
                      index=index)
            self._engine.dispose()
        except Exception as e:
            _Error_log.write(e)
            err = e
        return err

    def execute_sql(self, sql: str) -> Exception:
        _Query_log.write(sql)
        err = None
        try:
            if self._connectionString.dbconfig.driver == _OdbcDrivers.SQLite:
                self._connection = \
                    _sqlite3.connect(self._connectionString.dbconfig.database)
            else:
                self._connection = _po.connect(self._connectionString.get_odbc)
            self.Cursor = self._connection.cursor()
            self.Cursor.execute(sql)
            self._connection.commit()
            self.Cursor.close()
            self._connection.close()
        except Exception as e:
            _Error_log.write(e)
            err = e
        return err

    def load_all_excel_sheets_to_db(self, excel_file):
        err = None
        f = _pd.ExcelFile(excel_file)
        for sheet in f.sheet_names:
            try:
                df = f.parse(sheet)
                self.dataframe_to_db(df, sheet)
            except Exception as e:
                _Error_log.write(e)
                err = e
        return err

    def load_excel_sheet_to_db(self, excel_file, sheet_name):
        err = None
        f = _pd.ExcelFile(excel_file)
        for sheet in f.sheet_names:
            if sheet == sheet_name:
                try:
                    df = f.parse(sheet)
                    self.dataframe_to_db(df, sheet)
                except Exception as e:
                    _Error_log.write(e)
                    err = e
        return err

    def load_csv_to_db(self, csv_file, table_name):
        err = None
        try:
            df = _pd.read_csv(csv_file)
            self.dataframe_to_db(df, table_name)
        except Exception as e:
            _Error_log.write(e)
            err = e
        return err

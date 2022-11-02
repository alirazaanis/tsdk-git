"""
Telecom Systems Development Kit - tsdk
"""

import pandas as _pd

from tsdk.common.dbconfig import DbConfig as _DbConfig
from tsdk.common.dbconfig import OdbcDrivers as _OdbcDrivers
from tsdk.common.dbmanager import SQLServer as _SQLServer
from tsdk.common.logs import ErrorLog as _Error_log

__all__ = ['copy_data']


def copy_data(source: _DbConfig, destination: _DbConfig) -> Exception:
    err = None
    try:
        source_db = _SQLServer(source)
        destination_db = _SQLServer(destination)
        sql = "SELECT TABLE_NAME AS name FROM INFORMATION_SCHEMA.TABLES" \
            if (source.driver == _OdbcDrivers.MicrosoftSQLServer) \
            else "SELECT name FROM sqlite_master WHERE type='table'"
        tables, err = source_db.sql_to_dataframe(sql)
        if len(err.__class__.__name__) > 0:
            return err
        for index, row in tables.iterrows():
            print(row["name"])
            try:
                conn = source_db.Connection
                for chunk in _pd.read_sql("SELECT * FROM " + row["name"],
                                          con=conn,
                                          chunksize=50000):
                    engine = destination_db.Engine
                    chunk.to_sql(row["name"],
                                 con=engine,
                                 if_exists='append',
                                 index=False)
                    engine.dispose()
                conn.close()
                if destination.driver == _OdbcDrivers.MicrosoftSQLServer:
                    err = destination_db.execute_sql(
                        "DROP TABLE IF EXISTS temp_name")
                    if len(err.__class__.__name__) > 0:
                        _Error_log.write(err)
                    err = destination_db.execute_sql(
                        "SELECT DISTINCT * INTO temp_name FROM " + row["name"])
                    if len(err.__class__.__name__) > 0:
                        _Error_log.write(err)
                    err = destination_db.execute_sql(
                        "DROP TABLE IF EXISTS " + row["name"])
                    if len(err.__class__.__name__) > 0:
                        _Error_log.write(err)
                    err = destination_db.execute_sql(
                        "EXEC sp_rename temp_name, " + row["name"] + "")
                    if len(err.__class__.__name__) > 0:
                        _Error_log.write(err)
                else:
                    err = destination_db.execute_sql(
                        "DROP TABLE IF EXISTS temp_name")
                    if len(err.__class__.__name__) > 0:
                        _Error_log.write(err)
                    err = destination_db.execute_sql(
                        "CREATE TABLE temp_name AS SELECT DISTINCT * FROM " + row["name"] + ";")
                    if len(err.__class__.__name__) > 0:
                        _Error_log.write(err)
                    err = destination_db.execute_sql(
                        "DROP TABLE IF EXISTS " + row["name"] + ";")
                    if len(err.__class__.__name__) > 0:
                        _Error_log.write(err)
                    err = destination_db.execute_sql(
                        "ALTER TABLE temp_name RENAME TO " + row["name"] + "")
                    if len(err.__class__.__name__) > 0:
                        _Error_log.write(err)
            except Exception as e:
                _Error_log.write(e)
                err = e
                continue
    except Exception as e:
        _Error_log.write(e)
        err = e
    return err

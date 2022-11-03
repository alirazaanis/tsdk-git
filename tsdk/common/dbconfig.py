"""
Telecom Systems Development Kit - tsdk
"""

import urllib.parse as _parse
from enum import Enum as _Enum

__all__ = ['OdbcDrivers',
           'DbConfig',
           'ConnectionString']


class OdbcDrivers(_Enum):
    """ODBC Drivers Enumerator
    """
    MicrosoftSQLServer = 0
    SQLite = 1


def get_odbc_driver_str(odbc_driver: OdbcDrivers) -> str:
    """Get ODBC Driver Name

    Args:
        odbc_driver (OdbcDrivers): ODBC driver from OdbcDrivers Enum

    Returns:
        str: ODBC Driver name
    """
    if odbc_driver is OdbcDrivers.SQLite:
        return "SQLite3 ODBC Driver"
    elif odbc_driver is OdbcDrivers.MicrosoftSQLServer:
        return "ODBC Driver 17 for SQL Server"
    else:
        return "ODBC Driver 17 for SQL Server"


def get_odbc_driver(driver: str) -> OdbcDrivers:
    """Get ODBC Driver Name

    Args:
        driver (str): ODBC driver String

    Returns:
        OdbcDrivers: ODBC driver from OdbcDrivers Enum
    """
    if driver == "SQLite3 ODBC Driver":
        return OdbcDrivers.SQLite
    elif driver == "ODBC Driver 17 for SQL Server":
        return OdbcDrivers.MicrosoftSQLServer
    else:
        return OdbcDrivers.MicrosoftSQLServer


class DbConfig(object):
    """Database Configuration Object

    Args:
        driver (OdbcDrivers): ODBC driver from OdbcDrivers Enum
        server (str): Server Address
        database (str): Database Name
        uid (str): User Id
        pwd (str): Password
        trusted (bool): Trusted = Yes If using local authentication

    Properties:
        All parameters are available as Get/Set properties
    """

    def __init__(self,
                 driver: OdbcDrivers = OdbcDrivers.MicrosoftSQLServer,
                 server: str = "",
                 database: str = "",
                 uid: str = "",
                 pwd: str = "",
                 trusted: bool = False) -> None:
        """
        Initialize Database Configuration
        """
        self.driver: OdbcDrivers = driver
        self.server: str = server
        self.database: str = database
        self.uid: str = uid
        self.pwd: str = pwd
        self.trusted: bool = trusted

    def parse_odbc(self, odbc: str):
        keys_by_semicolon = odbc.split(";")
        conn_string_keys = {}
        for key_semicolon in keys_by_semicolon:
            keys_by_equals = key_semicolon.split("=")
            if len(keys_by_equals) == 1:
                conn_string_keys[keys_by_equals[0].upper()] = ""
            elif len(keys_by_equals) == 2:
                conn_string_keys[keys_by_equals[0].upper()] = keys_by_equals[1]
        if "DRIVER" in conn_string_keys:
            self.driver = get_odbc_driver(conn_string_keys["DRIVER"].lstrip("{").rstrip("}"))
        if "DATA SOURCE" in conn_string_keys:
            self.server = conn_string_keys["DATA SOURCE"]
        if "DATABASE" in conn_string_keys:
            self.database = conn_string_keys["DATABASE"]
        if "INITIAL CATALOG" in conn_string_keys:
            self.database = conn_string_keys["INITIAL CATALOG"]
        if "USER ID" in conn_string_keys:
            self.uid = conn_string_keys["USER ID"]
        if "PASSWORD" in conn_string_keys:
            self.pwd = conn_string_keys["PASSWORD"]
        if "INTEGRATED SECURITY" in conn_string_keys:
            self.trusted = True


class ConnectionString(object):
    """Connection String Object

    Args:
        dbconfig (DbConfig): Server Configuration Parameters in DbConfig Structure

    Properties:
        get_odbc:
            Returns:
                str: ODBC Connection String for pyodbc

        get_url:
            Returns:
                str: DSN style Connection String for sqlalchemy Engine

    """

    def __init__(self, dbconfig: DbConfig) -> None:
        """
        Initialize Connection String
        """
        self.dbconfig = DbConfig(dbconfig.driver,
                                 dbconfig.server,
                                 dbconfig.database,
                                 dbconfig.uid,
                                 dbconfig.pwd,
                                 dbconfig.trusted)

    @property
    def get_odbc(self) -> str:
        """Get ODBC

        Returns:
            str: ODBC Connection String for pyodbc
        """
        return str("DRIVER={" + get_odbc_driver_str(self.dbconfig.driver) + "};" +
                   "SERVER=" + self.dbconfig.server + ";" +
                   "DATABASE=" + self.dbconfig.database + ";" +
                   "TRUSTED_CONNECTION=YES" if self.dbconfig.trusted else
                   "DRIVER={" + get_odbc_driver_str(self.dbconfig.driver) + "};" +
                   "SERVER=" + self.dbconfig.server + ";" +
                   "DATABASE=" + self.dbconfig.database + ";" +
                   "UID=" + self.dbconfig.uid + ";" +
                   "PWD=" + self.dbconfig.pwd + ";")

    @property
    def get_url(self) -> str:
        """Get Url

        Returns:
            str: DSN style Connection String for sqlalchemy Engine
        """
        if self.dbconfig.driver == OdbcDrivers.MicrosoftSQLServer:
            params = _parse.quote_plus(
                "DRIVER={" + get_odbc_driver_str(self.dbconfig.driver) + "};" +
                "SERVER=" + self.dbconfig.server + ";" +
                "DATABASE=" + self.dbconfig.database + ";" +
                "TRUSTED_CONNECTION=YES" if self.dbconfig.trusted else
                "DRIVER={" + get_odbc_driver_str(self.dbconfig.driver) + "};" +
                "SERVER=" + self.dbconfig.server + ";" +
                "DATABASE=" + self.dbconfig.database + ";" +
                "UID=" + self.dbconfig.uid + ";" +
                "PWD=" + self.dbconfig.pwd)
            return str("mssql+pyodbc:///?odbc_connect=%s" % params)
        else:
            return str("sqlite:///" + self.dbconfig.database)

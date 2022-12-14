# tsdk-git





## Install


```
pip install tsdk-git==5.3.3
```



## Usage


### Copy database example


```
from tsdk import *
source = DbConfig(OdbcDrivers.SQLite, "10.10.10.10", "database1", "uid", "pwd", False)
destination = DbConfig(OdbcDrivers.MicrosoftSQLServer, "10.10.10.10", "database2", "uid", "pwd", False)
copy_data(source, destination)
```


### Server object example


#### Set TsdkServer configuration


```
s = TsdkServer()
s.set_configuration(OdbcDrivers.MicrosoftSQLServer, "desktop-v8venfm", "tsdk", "sa", "root", False)
s.set_configuration(OdbcDrivers.MicrosoftSQLServer, "desktop-v8venfm", "tsdk", "", "", True)
```


#### Save configuration


Save to custom file


```
s.save_configuration("conf_test.json")
```


Save to default file


```
s.save_configuration()
```


#### Setup TsdkServer System Tables


Safely call this function for the first time,
Should be used with care, it will delete exsisting system tables


```
s.setup_database()
```


#### Export/Import System Tables


Find sample system tables in release v1.0.0 Assets


Export system tables to Excel file


Call setup_database before exporting system tables for the first time


```
s.export_system_tables(r"c:/users/ali/desktop/tsdk_system_tables.xlsx")
```


Import system tables from Excel file,


Should be used with care, it will overwrite existing system tables


```
s.import_system_tables(r"c:/users/ali/desktop/tsdk_system_tables.xlsx")
```


#### Execute SQL statement on SQL server


```
s.execute_sql("select * from table")
```


#### Load database table to dataframe


return tuple df, err


```
df, err = s.sql_to_dataframe("select * from table")
```


#### Load dataframe to database table


```
s.dataframe_to_sql(df, "table_name", index=False)
```


#### Load Excel file with multiple sheets to database tables,


Sheet names will be used as table name


```
s.load_all_excel_sheets_to_db(excel_file)
```


#### Load Excel sheet to database table


```
s.load_excel_sheet_to_db(excel_file, sheet_name)
```


#### Load CSV file to database table


```
s.load_csv_to_db(csv_file, table_name)
```


#### Run Audit


```
nr_basic_audit_v2()
```


#### Run Scheduler


```
sch = TsdkScheduler(jobs_df=s.sql_to_dataframe("Select * from scheduler")[0])
sch.start()
```

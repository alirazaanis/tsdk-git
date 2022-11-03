from tsdk import *
# from tsdk import nr_basic_audit_v2

if __name__ == '__main__':
    print("test")
    # copy database example
    # source = DbConfig(OdbcDrivers.SQLite, "10.10.10.10", "database1", "uid", "pwd", False)
    # destination = DbConfig(OdbcDrivers.MicrosoftSQLServer, "10.10.10.10", "database2", "uid", "pwd", False)
    # copy_data(source, destination)

    # server object example
    s = TsdkServer()
    s.set_configuration(OdbcDrivers.MicrosoftSQLServer, "desktop-v8venfm", "tsdk", "sa", "root", False)
    s.set_configuration(OdbcDrivers.MicrosoftSQLServer, "desktop-v8venfm", "tsdk", "", "", True)
    s.save_configuration("conf_test.json")
    s.setup_database()
    # s.export_system_tables(r"c:/users/ali/desktop/tsdk_system_tables.xlsx")
    s.import_system_tables(r"c:/users/ali/desktop/tsdk_system_tables.xlsx")
    # s.execute_sql("")
    # df1 = s.sql_to_dataframe("")
    # s.dataframe_to_sql_2(df1, "ada", index=False)
    # s.load_all_excel_sheets_to_db(excel_file)
    # s.load_excel_sheet_to_db(excel_file)
    # s.load_csv_to_db(csv_file)

    # t = TsdkServer()
    # t.set_configuration(OdbcDrivers.SQLite, "10.10.10.10", "Ericsson5g", "uid", "pwd", True)
    # s.save_configuration()
    # s.execute_sql("")
    # s.dataframe_to_sql(df1, "ada", index=False)

    nr_basic_audit_v2()

    sch = TsdkScheduler(jobs_df=s.sql_to_dataframe("Select * from scheduler")[0])
    sch.start()

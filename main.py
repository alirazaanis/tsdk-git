# from tsdk import *
# from tsdk import nr_basic_audit_v2

if __name__ == '__main__':
    print("test")
    # copy database example
    # source = DbConfig(OdbcDrivers.SQLite, "10.10.10.10", "database1", "uid", "pwd")
    # destination = DbConfig(OdbcDrivers.MicrosoftSQLServer, "10.10.10.10", "database2", "uid", "pwd")
    # copy_data(source, destination)

    # server object example
    # s = TsdkServer()
    # s.set_configuration(OdbcDrivers.SQLite, "10.10.10.10", "Ericsson4g", "uid", "pwd", True)
    # s.save_configuration()
    # s.execute_sql("")
    # df1 = s.sql_to_dataframe("")
    # s.dataframe_to_sql(df1, "ada", index=False)

    # t = TsdkServer()
    # t.set_configuration(OdbcDrivers.SQLite, "10.10.10.10", "Ericsson5g", "uid", "pwd", True)
    # s.save_configuration()
    # s.execute_sql("")

    # sch = TsdkScheduler(jobs_df=s.sql_to_dataframe("Select * from scheudler"))
    # sch.start()

    # s.dataframe_to_sql(df1, "ada", index=False)

    # nr_basic_audit_v2()

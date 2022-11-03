from tsdk import Logics as _Logics
from tsdk import LogicsLogSchemaParams as _Llsp
from tsdk import LogicsSchemaParams as _Lsp
from tsdk import SystemSchemas as _Ss
from tsdk import TsdkServer as _Tsdk

__all__ = ['nr_basic_audit_v2']


def nr_basic_audit_v2():
    tsdk = _Tsdk()
    df, err = tsdk.sql_to_dataframe(
        "SELECT * FROM " + _Ss.Logics +
        " WHERE LOWER(" + _Lsp.LogicName +
        ") Like '%" + _Logics.NR_Basic_Audit_V2 +
        "%'")
    df.columns = map(str.lower, df.columns)
    df = df.astype(str)
    for index, row in df.iterrows():
        if str(row[_Lsp.Enabled]).lower() == "true":
            # family = "(SELECT T1.* FROM " + row[_LogicParams.Family] + " T1 " + \
            #         "INNER JOIN (" + \
            #         "SELECT NodeId, MAX(CAST(DateList_id AS bigint)) DateList_id FROM " + \
            #         row[_LogicParams.Family] + " GROUP BY NodeId" + \
            #         ") T2 ON " + \
            #         "T2.NodeId = T1.NodeId AND " + \
            #         "T1.DateList_id = T1.DateList_id)"
            family = row[_Lsp.Family]

            if str(row[_Lsp.ParameterValue]).lower() == "true":
                check = "(LOWER(CAST(" + row[_Lsp.Parameter] + " AS VARCHAR)) " + \
                        "<> " + \
                        "'" + str(row[_Lsp.ParameterValue]).lower() + "' AND " + \
                        "LOWER(CAST(" + row[_Lsp.Parameter] + " AS VARCHAR)) " + \
                        "<> " + \
                        "'1')"
            elif str(row[_Lsp.ParameterValue]).lower() == "false":
                check = "(LOWER(CAST(" + row[_Lsp.Parameter] + " AS VARCHAR)) " + \
                        "<> " + \
                        "'" + str(row[_Lsp.ParameterValue]).lower() + "' AND " + \
                        "LOWER(CAST(" + row[_Lsp.Parameter] + " AS VARCHAR)) " + \
                        "<> " + \
                        "'0')"
            else:
                check = "(LOWER(CAST(" + row[_Lsp.Parameter] + " AS VARCHAR)) " + \
                        "<> " + \
                        "'" + str(row[_Lsp.ParameterValue]).lower() + "')"

            sql = "SELECT " \
                  "'" + row[_Lsp.LogicName] + "' AS " + _Llsp.LogicName + ", " + \
                  "'" + row[_Lsp.Family] + "' AS " + _Llsp.Family + ", " + \
                  "'" + row[_Lsp.Database] + "' AS '" + _Llsp.Database + "', " + \
                  "'" + row[_Lsp.LayerTechnology] + "' AS " + _Llsp.LayerTechnology + ", " + \
                  row[_Lsp.MOKey] + " AS " + _Llsp.MOKey + ", " + \
                  "'" + row[_Lsp.Parameter] + "' AS " + _Llsp.Parameter + ", " + \
                  row[_Lsp.Parameter] + " AS " + _Llsp.OldValue + ", " \
                                                                  "'" + row[
                      _Lsp.ParameterValue] + "' AS " + _Llsp.NewValue + ", " + \
                  " GETDATE() AS " + _Llsp.Time + ", " + \
                  " CAST( GETDATE() AS Date ) AS " + _Llsp.Date + " " + \
                  " FROM " + family + \
                  " T3 WHERE " + check

            if str(row[_Lsp.ExcludedNEs]).lower() == "yes":
                sql += " AND " + _Lsp.MOKey + \
                       " NOT IN (SELECT * FROM tsdk.dbo." + _Ss.ExcludeNEs + ")"

            if str(row[_Lsp.FreeSQL]).lower() != "nan" and \
                    str(row[_Lsp.FreeSQL]).lower() != "none":
                sql += " AND " + _Lsp.MOKey + " IN (SELECT " + _Lsp.MOKey + " FROM (" + \
                       row[_Lsp.FreeSQL] + ") T)"

            sqldb = _Tsdk()
            sqldb.ConnectionString.dbconfig.database = row[_Lsp.Database]

            df2, err = sqldb.sql_to_dataframe(sql)

            err = tsdk.dataframe_to_db(df2, _Ss.LogicsLogs)

    return err

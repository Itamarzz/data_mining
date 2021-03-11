import pymysql
import pandas as pd

def connect_sql(host = 'localhost', user = 'root', password = 'root'):
    """ connect pymysql
    """
    con = pymysql.connect(host = host, user = user, password = password)
    return con


def execute_sql(sql_string, con):
    """ execute sql statement
    """
    cur = con.cursor()
    cur.execute(sql_string)
    cur.close()


def sql_query(sql_string, con):
    """ returns df of sql query
    """

    cur = con.cursor()
    cur.execute(sql_string)
    result = cur.fetchall()
    cur.close()

    df = pd.DataFrame(result)

    return df


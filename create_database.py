import pymysql
import config.database_config as dbc
import sys
from config import database_config as dbcfg


def connect_sql(host=dbc.HOST, user=dbc.USERNAME, password=dbc.PASSWORD):
    """ connect pymysql
    """

    try:
        con = pymysql.connect(host=host, user=user, password=password)
        return con
    except pymysql.err.OperationalError as err:
        print("couldn't connect pymysql. please verify that host, username and \n"
              "password are all correct and try again", format(err))
        sys.exit(1)


def execute_sql(sql_string, con):
    """ execute sql statement
    """

    cur = con.cursor()
    cur.execute(sql_string)


def create_db():
    """ creating mysql database with given list of tables and references
    """

    con = connect_sql()
    execute_sql(dbc.CREATE_DATABASE, con)
    execute_sql(f"USE {dbcfg.DATABASE_NAME}", con)

    for table in dbc.CREATE_TABLES:
        execute_sql(table, con)


def use_database(databaseto_use=dbcfg.DATABASE_NAME):
    """ creates a connection and use to sql database
    """

    con = connect_sql()
    try:
        execute_sql(f"USE {databaseto_use}", con)
    except pymysql.err.OperationalError:
        print(f"Database {databaseto_use} was not found.\n"
              f"Please make sure you set the correct database name in database_config file.\n"
              f"if database is not exists please create first. find more information in README")
        sys.exit(1)

    return con


create_db()

# TESTS

# create_db()
# con = connect_sql(dbc.HOST, dbc.USERNAME, dbc.PASSWORD)

# execute_sql("USE proballers", con)

# for table in dbc.TABLE_NAMES[::-1]:
#     execute_sql(f'drop table {table}', con)

# execute_sql("drop database proballers", con)
#
# print(sql_query("show databases", con))


# # print(sql_query("show tables", con))

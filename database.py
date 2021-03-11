import pymysql
import pandas as pd
import config.database_config as dbc
import sys


def connect_sql(host=dbc.HOST, user=dbc.USERNAME, password=dbc.PASSWORD):
    """ connect pymysql
    """

    try:
        con = pymysql.connect(host=host, user=user, password=password)
        return con
    except Exception:
        print("couldn't connect pymysql. please verify that host, username and password are all correct and try again")
        sys.exit(1)


def execute_sql(sql_string, con):
    """ execute sql statement
    """
    cur = con.cursor()
    try:
        cur.execute(sql_string)
    except Exception:
        print("couldn't execute the SQL query. please make sure it's written correctly in mysql")
        sys.exit(1)
    finally:
        cur.close()


def sql_query(sql_string, con):
    """ returns df of sql query
    """

    cur = con.cursor()
    try:
        cur.execute(sql_string)
        result = cur.fetchall()
        df = pd.DataFrame(result)
    except Exception:
        print("couldn't execute the SQL query. please make sure it's written correctly in mysql")
        sys.exit(1)
    finally:
        cur.close()

    return df


# def get_sql_cred():
#     USERNAME = input('please enter user:')
#     PASSWORD = input('Password:')
#
#     return USERNAME, PASSWORD


def create_db():
    """ creating mysql database with given list of tables and references
    """
    con = connect_sql()
    execute_sql(dbc.CREATE_DATABASE, con)
    print('database was created successfully')
    execute_sql("USE proballers", con)

    for table in dbc.CREATE_TABLES:
        execute_sql(table, con)

    print('\nall tables were created successfully')


def main():
    create_db()


if __name__ == '__main__':
    main()

########### TESTS ##########################

# create_db()
# con = connect_sql(dbc.HOST, dbc.USERNAME, dbc.PASSWORD)

# execute_sql("USE proballers", con)

# for table in dbc.TABLE_NAMES[::-1]:
#     execute_sql(f'drop table {table}', con)

# execute_sql("drop database proballers", con)
#
# print(sql_query("show databases", con))


# # print(sql_query("show tables", con))






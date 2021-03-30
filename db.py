from config import database_config as dbcfg
import pandas as pd
import pymysql
import config.database_config as dbc
import sys
from sqlalchemy import create_engine


def get_df(data):
    """Returns a data frame
    """
    df = pd.DataFrame.from_dict(data, orient='index')

    return df


def assign_types_to_df(df, table):
    """ Assign type to data according to table definitions in db
    """
    types = dbcfg.TABLES[table]
    for col, field_type in types.items():
        if field_type == 'date':
            df[col] = pd.to_datetime(df[col])
        else:
            df[col] = df[col].astype(field_type)

    return df[types.keys()]


def insert_dict_to_df(data_dict, chunk_size):
    """ inserts data into tables in the database.
    input: dictionary where keys are table names and values are dictionaries with data to insert to table
    """

    engine = create_engine_con()
    for table, data in data_dict.items():
        if data:
            df = get_df(data)
            df = assign_types_to_df(df, table)
            df.to_sql(name=table, con=engine, if_exists='append', chunksize=chunk_size, index=False)


# pymsql usful functions

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


def create_engine_con():
    """ creating connection to mysql database
    """
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user=dbcfg.USERNAME,
                                   pw=dbcfg.PASSWORD,
                                   db=dbcfg.DATABASE_NAME))

    return engine

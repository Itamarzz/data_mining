from config import database_config as dbcfg
import pandas as pd
import pymysql
import config.database_config as dbc
import sys
from sqlalchemy import create_engine
import logging


def set_logger():
    """ set scraper module logger
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(dbcfg.LOG_FILE)
    file_handler.setFormatter(dbcfg.MAIN_FORMATTER)

    logger.addHandler(file_handler)

    return logger


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
            db_logger.info(f'data frame of table {table} has been created successfully')
            df = assign_types_to_df(df, table)
            db_logger.info(f'data type processing of table {table} - success')
            df.to_sql(name=table, con=engine, if_exists='append', chunksize=chunk_size, index=False)
            db_logger.info(f'data of {table} has been inserted to db successfully')
        else:
            db_logger.info(f'no data to insert to table {table} ')


def connect_sql(host=dbc.HOST, user=dbc.USERNAME, password=dbc.PASSWORD):
    """ connect pymysql
    """

    try:
        con = pymysql.connect(host=host, user=user, password=password)
        return con
    except pymysql.err.OperationalError as err:
        print("couldn't connect pymysql. please verify that host, username and \n"
              "password are all correct and try again", format(err))
        db_logger.error(f' connection to pymysql failed')
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
        db_logger.error(f' database {databaseto_use} not found')
        sys.exit(1)

    db_logger.info(f'connected to database {databaseto_use} successfully')

    return con


def create_engine_con():
    """ creating connection to mysql database
    """
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user=dbcfg.USERNAME,
                                   pw=dbcfg.PASSWORD,
                                   db=dbcfg.DATABASE_NAME))

    db_logger.info(f'created engine to connect mysql successfully')

    return engine


db_logger = set_logger()

import database_config as dbc
import database as db

con = db.connect_sql(dbc.HOST, dbc.USERNAME, dbc.PASSWORD)

# db.execute_sql(dbc.CREATE_DATABASE, con)

# print(db.sql_query("show databases", con))

db.execute_sql("use proballers", con)

# for table in dbc.CREATE_TABLES:
#     db.execute_sql(table, con)

# for ref in dbc.CREATE_REF:
#     db.execute_sql(ref, con)

# for table in dbc.TABLE_NAMES:
#     print()
#     print(db.sql_query(f"describe {table}", con))

# for table in dbc.TABLE_NAMES[::-1]:
#     db.execute_sql(f'drop table {table}', con)

# db.execute_sql("drop database proballers", con)

# print(db.sql_query("show tables", con))

from db_utils import excute_query
import pymysql

def create_task(keys, values):

    params = ', '.join(['%s'] * len(values))
    sql_create = "INSERT INTO tasks (id, title, description, done)" \
    "VALUES (1, %s, %s, False);"
    excute_query(sql_create, params)

import pymysql


def excute_query(sql, params=None, fetch=True):
    conn = pymysql.connect(
        host='todo_db',
        user='mysql',
        password='mysql',
        db='todo_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            if fetch:
                result = fetch.all()
            else:
                result = None
        conn.commit()
    finally:
        conn.close()
    return result

# 呼び出し例
# sql1 = "SELECT * FROM users WHERE id = %s"
# users = execute_query(sql1, (1,))

# sql2 = "UPDATE users SET name = %s WHERE id = %s"
# execute_query(sql2, ('新しい名前', 1), fetch=False)

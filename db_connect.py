import pymysql

def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host='localhost',
            database='mydb',
            user='root',
            password='',
            charset='utf8mb4',
            cursorclass =pymysql.cursors.DictCursor
        )
        # cursor = conn.cursor()
        # sqlQuery = """create table todo (id integer primary key, title text not null,task text not null)"""
        # cursor.execute(sqlQuery)  # run the file again
        # conn.close()
    except pymysql.Error as e:
        print('error from remote db', e)
    return conn

# conn = pymysql.connect(
#     host='localhost',
#     database='mydb',
#     user='root',
#     password='',
#     charset='utf8mb4',
#     cursorclass =pymysql.cursors.DictCursor
# )  # run the file

# cursor = conn.cursor()
# sqlQuery = """create table todo (id integer primary key, title text not null,task text not null)"""
# cursor.execute(sqlQuery)  # run the file again

# conn.close()

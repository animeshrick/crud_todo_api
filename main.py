from flask import Flask,request,jsonify
import pymysql.cursors
# from db_connect import db_connection


app = Flask(__name__)


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
    except pymysql.Error as e:
        print('error from remote db', e)
    return conn

def on_success(value):
    if value != '':
        success = {"status":200,"data":value}
        return jsonify((success)), 200

def on_error(value):
    if value != '':
        failed = {"status":500,"data":value}
        return jsonify((failed)), 500


@app.route("/v1/getAllTodo", methods=["GET"])
def get_all_todo():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        resultFromDb = cursor.execute("select * from todo")
        if resultFromDb != 0:
            for i in range(resultFromDb):
                return on_success(cursor.fetchall())
        else:
            return on_error('Nothinng to show')

@app.route("/v1/addTodo", methods=["POST"])
def add_todo():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        new_title = request.form['title']              
        new_task = request.form['task']
        resultFromDb = cursor.execute("select * from todo")                     
        if new_title == '':
            return on_error('Cant add empty title')
        elif new_task == '':
            return on_error('Cant add empty task')
        elif resultFromDb != 0:
            for i in range(resultFromDb):
                all_data = cursor.fetchall()[i]['title']
                if all_data == new_title:
                    return on_error('Cant add same title')
                else:
                    resultFromDb = cursor.execute("INSERT INTO todo (title,task) VALUES(%s,%s)", (new_title,new_task,))
                    conn.commit()
                    return on_success('Your data is addded')
        else:
            resultFromDb = cursor.execute("INSERT INTO todo (title,task) VALUES(%s,%s)", (new_title,new_task,))
            conn.commit()
            return on_success('Your data is addded')

@app.route('/v1/updateTodo/<int:id>', methods=["POST"])
def update_todo(id):
    conn = db_connection()
    cursor = conn.cursor()
    id_query = 'select (1) from todo where id = %s'
    id_val =  cursor.execute(id_query,(id))
    if id_val == 0:
        return on_error(f'{id} is not valid id')
    elif id != 0 and id != '':
        if request.method == "POST":
            update_task = request.form['task']
            if update_task == '':
                return on_error('Cant add empty task')
            else:
                query = 'update todo set task = %s where id = %s'
                value = (update_task,id)
                cursor.execute(query,value)
                conn.commit()
            return on_success(f"Your task {id} is updated")
        
@app.route('/v1/deleteTodo/<int:id>', methods=["POST"])
def delete_todo(id):
     if id != 0 and id != '':
        conn = db_connection()
        cursor = conn.cursor()
        if request.method == "POST":
            del_query = 'DELETE FROM todo WHERE id = %s'
            cursor.execute(del_query,(id))
            conn.commit()
            return on_success(f"Your task {id} is deleted")
                        


if __name__ == '__main__':
    app.run(port=2023)

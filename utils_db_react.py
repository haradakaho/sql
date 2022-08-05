import psycopg2
import conf
from flask import Flask, request, jsonify
import uuid

api = Flask(__name__)

# Global Variable
todolist = ["id", "name", "completed"]

#DB接続
def get_connection():
    con = psycopg2.connect( 
        host = conf.host,
        password = conf.password,
        user = conf.user,
        port = conf.port)
    
    #DB接続確認
    if con is not None:
        print("Connection Success !")
    else:
        print("Connection Error !")
    
    return con

@api.route('/_health', methods=['GET'])
def health_check():
    return "OK"

@api.route('/insert', methods=['POST'])
def insert_test_item():
    con = None
    try:
        # Request Validation
        if "id" in request.get_json():
            try:
                uuid.UUID(str(request.get_json()["id"]))
            except ValueError:
                request.get_json()["id"] = str(uuid.uuid4())
        else:
            request.get_json()["id"] = str(uuid.uuid4())
        
        if "name" not in request.get_json():
            res_err = {
                "status": "Error",
                "message": "Bad Request: name is None"
            }
            return res_err, 400

        if "completed" not in request.get_json():
            res_err = {
                "status": "Error",
                "message": "Bad Request: completed is None"
            }
            return res_err, 400
        
        id = request.get_json()["id"] 
        name = request.get_json()["name"]
        completed = '1' if request.get_json()["completed"] else '0'

        con = get_connection()
        if con is not None:
            cur = con.cursor()
            insert_sql = ""
            if "id" in request.get_json():
                select_sql = "SELECT COUNT(1) FROM todo where id = %s"
                cur.execute(select_sql, (id,))
                row = cur.fetchone()

                if row:
                    if row[0] > 0:
                        id = str(uuid.uuid4())
                insert_sql += "INSERT INTO Todo (id, name, completed, createdAt, updatedAt) VALUES(%s, %s, %s, %s, %s)"
                cur.execute(insert_sql, (id, name, completed, "NOW()", "NOW()"))

            else:
                insert_sql += "INSERT INTO Todo (name, completed, createdAt, updatedAt) VALUES(%s, %s, %s, %s)"
                cur.execute(insert_sql, (name, completed, "NOW()", "NOW()"))
            con.commit()

            # Close communication with the database
            cur.close()
            con.close()

            res = {
                "status": "201",
                "message": "New test was inserted successfully"
            }
            return res, 201
        else:
            res_err = {
                "status": "Error",
                "message": "Connection is None"
            }
            return res_err, 502
    
    except Exception as error:
        if con is not None:
            con.rollback()
            con.close()
        res_err = {
            "status": "Error",
            "message": "Unexpected Error : {}".format(error)
        }
        return res_err, 500

@api.route('/select', methods=['GET'])   
def find():
    con = None
    try:
        # Request Validation => id
        if "id" not in request.args:
            res_err = {
                "status": "Error",
                "message": "Bad Request: id is None"
            }
            return res_err, 400
        
        con = get_connection() 
        if con is not None:
            cur = con.cursor()
            cur.execute("SELECT id, name, completed, updatedAt, createdAt FROM Todo WHERE id = %s",(request.args['id'],))
            row = cur.fetchone()
            if row:
                res = dict()
                res["status"] = "success"
                todo = dict()
                todo["id"] = row[0]
                todo["name"] = row[1]
                todo["completed"] = row[2]
                todo["updatedAt"] = row[3]
                todo["createdAt"] = row[4]

                res["todo"] = todo

                # Close communication with the database
                cur.close()
                con.close()
                return jsonify(res), 200
            else:
                # Close communication with the database
                cur.close()
                con.close()
                res_err = {
                    "status": "error",
                    "message": "todo {} is None".format((request.args['id']))
                }
                return res_err, 400
            
        else:
            res_err = {
                "status": "Error",
                "message": "Connection is None"
            }
            return res_err, 502

    except Exception as error:
        if con is not None:
            con.rollback()
            con.close()
        res_err = {
            "status": "Error",
            "message": "Unexpected Error : {}".format(error)
        }
        return res_err, 500

@api.route('/selectall', methods=['GET'])   
def select_all():
    con = None
    try:
        con = get_connection() 
        if con is not None:
            cur = con.cursor()
            cur.execute("SELECT id, name, completed, updatedAt, createdAt FROM Todo")
            rows = cur.fetchall()
            res = dict()
            res["status"] = "success"
            res["todolist"] = []
            print(rows)
            if len(rows) > 0:
                for row in rows:
                    todo = dict()
                    todo["id"] = row[0]
                    todo["name"] = row[1]
                    todo["completed"] = row[2]
                    todo["updatedAt"] = row[3]
                    todo["createdAt"] = row[4]

                    res["todolist"].append(todo)

                # Close communication with the database
                cur.close()
                con.close()
                return jsonify(res), 200
            else:
                # Close communication with the database
                cur.close()
                con.close()
                res_err = {
                    "status": "error",
                    "message": "test {} is None".format((request.args['id']))
                }
                return res_err, 400
            
        else:
            res_err = {
                "status": "Error",
                "message": "Connection is None"
            }
            return res_err, 502

    except Exception as error:
        if con is not None:
            con.rollback()
            con.close()
        res_err = {
            "status": "Error",
            "message": "Unexpected Error : {}".format(error)
        }
        return res_err, 500

@api.route('/update', methods=['POST'])
def update_test_item():
    con = None
    try:
        # Request Validation
        if "id" not in request.get_json():
            res_err = {
                "status": "Error",
                "message": "Bad Request: id is None"
            }
            return res_err, 400
        
        if "name" not in request.get_json()["update_content"]:
            res_err = {
                "status": "Error",
                "message": "Bad Request: nameis None"
            }
            return res_err, 400

        if "completed" not in request.get_json()["update_content"]:
            res_err = {
                "status": "Error",
                "message": "Bad Request: completed is None"
            }
            return res_err, 400

        # id = request.get_json()["id"] 
        # name = request.get_json()["update_content"]["name"]
        
        con = get_connection()
        if con is not None:
            cur = con.cursor()

            # Make sql to update
            update_sql = "UPDATE Todo SET "
            bind_object = []
            print(request.get_json()["update_content"])

            # Add column to be setted
            for key, value in request.get_json()["update_content"].items():
                if key in todolist:
                    print("key:" + key + " exists")
                    if key == "completed":
                        value = '1' if value else '0'
                    update_sql += "{} = %s, ".format(key)
                    bind_object.append(value)
                else:
                    print("WARNING key:" + key + " does not exist")
            
            update_sql += "updatedAt = NOW()"

            # Add WHERE condition
            update_sql += " WHERE id = %s"
            bind_object.append(request.get_json()["id"])
            print("Update SQL : " + update_sql)
            print("Bind Object : {}".format(bind_object))
            # print("Bind Object : " + str(bind_object))
            # print("Bind Object :", bind_object)

            cur.execute(update_sql, tuple(bind_object))
            con.commit()
            num = cur.rowcount
            res = {
                "status": "201",
                "message": "{} Todo were updated successfully".format(num)
            }
            # Close communication with the database
            cur.close()
            con.close()
            return res, 201

        else:
            res_err = {
                "status": "Error",
                "message": "Connection is None"
            }
            return res_err, 502

    except Exception as error:
        if con is not None:
            con.rollback()
            con.close()
        res_err = {
            "status": "Error",
            "message": "Unexpected Error : {}".format(error)
        }
        return res_err, 500

@api.route('/delete', methods=['POST'])
def delete_test_item():
    con = None
    try:
        con = get_connection()
        if con is not None:
            cur = con.cursor()
            
            # Execute sql to delete row
            delete_sql = "DELETE FROM Todo WHERE completed = '1' "
            bind_object = []

            # Add column to be setted
            if "id" in request.get_json():
                delete_sql += "AND {} = %s".format("id")
                bind_object.append(request.get_json()["id"])
        
            # Show in logs SQL details
            print("Delete SQL : " + delete_sql)
            print("Bind Object : {}".format(bind_object))
            
            # SQL execution
            cur.execute(delete_sql, tuple(bind_object))
            con.commit()
            num = cur.rowcount
            res = {
                "status": "201",
                "message": "{} Todo were deleted successfully".format(num)
            }
            # Close communication with the database
            cur.close()
            con.close()
            
            return res, 201

        else:
            res_err = {
                "status": "Error",
                "message": "Connection is None"
            }
            return res_err, 502
        
    except Exception as error:
        if con is not None:
            con.rollback()
            con.close()
        res_err = {
            "status": "Error",
            "message": "Unexpected Error : {}".format(error)
        }
        return res_err, 500

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=3001)
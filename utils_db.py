import psycopg2
import conf
from flask import Flask, request, jsonify

api = Flask(__name__)

# Global Variable
test_column = ["id", "num", "data"]

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

@api.route('/insert', methods=['POST'])
def insert_test_item():
    con = None
    try:
        # Request Validation => num, data
        if "num" not in request.get_json():
            res_err = {
                "status": "Error",
                "message": "Bad Request: num is None"
            }
            return res_err, 400

        if "data" not in request.get_json():
            res_err = {
                "status": "Error",
                "message": "Bad Request: data is None"
            }
            return res_err, 400
        
        con = get_connection()
        if con is not None:
            cur = con.cursor()

            insert_sql = "INSERT INTO test (num, data, createdAt, updatedAt) VALUES(%s, %s, %s, %s)"
            cur.execute(insert_sql, (request.get_json()["num"], request.get_json()["data"], "NOW()", "NOW()"))
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

@api.route('/select', methods=['POST'])   
def select_test_item():
    con = None
    try:
        # Request Validation => id
        if "id" not in request.get_json():
            res_err = {
                "status": "Error",
                "message": "Bad Request: id is None"
            }
            return res_err, 400
        
        try:
            int(request.get_json()["id"])
        except ValueError:
            res_err = {
                "status": "Error",
                "message": "Bad Request: id must be a number"
            }
            return res_err, 400
        
        con = get_connection() 
        if con is not None:
            cur = con.cursor()
            cur.execute("SELECT id, num, data, updatedAt, createdAt FROM test WHERE id = %s",(request.get_json()["id"],))
            row = cur.fetchone()
            if row:
                res = dict()
                res["status"] = "success"
                test_data = dict()
                test_data["id"] = row[0]
                test_data["num"] = row[1]
                test_data["data"] = row[2]
                test_data["updatedAt"] = row[3]
                test_data["createdAt"] = row[4]

                res["test_data"] = test_data

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
                    "message": "test {} is None".format(request.get_json()["id"])
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
        # Request Validation => id
        if "id" not in request.get_json():
            res_err = {
                "status": "Error",
                "message": "Bad Request: id is None"
            }
            return res_err, 400
        
        try:
            int(request.get_json()["id"])
        except ValueError:
            res_err = {
                "status": "Error",
                "message": "Bad Request: id must be a number"
            }
            return res_err, 400

        try:
            int(request.get_json()["num"])
        except ValueError:
            res_err = {
                "status": "Error",
                "message": "Bad Request: num must be a number"
            }
            return res_err, 400
        
        con = get_connection()
        if con is not None:
            cur = con.cursor()

            # Make sql to update
            update_sql = "UPDATE test SET "
            bind_object = []
            print(request.get_json()["update_content"])

            # Add column to be setted
            for key, value in request.get_json()["update_content"].items():
                if key in test_column:
                    print("key:" + key + " exists")
                    update_sql += "{} = %s, ".format(key)
                    bind_object.append(value)
                else:
                    return "WARNING key:" + key + " does not exist"
            
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
            
            # Close communication with the database
            cur.close()
            con.close()
            res = {
                "status": "201",
                "message": "Test {} was updated successfully".format(request.get_json()["id"])
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

@api.route('/delete', methods=['POST'])
def delete_test_item():
    con = None
    try:
        # Request Validation => id
        if "id" not in request.get_json():
            res_err = {
                "status": "Error",
                "message": "Bad Request: id is None"
            }
            return res_err, 400

        try:
            int(request.get_json()["id"])
        except ValueError:
            res_err = {
                "status": "Error",
                "message": "Bad Request: id must be a number"
            }
            return res_err, 400
        
        con = get_connection()
        if con is not None:
            cur = con.cursor()
            
            # Execute sql to delete row
            delete_sql = "DELETE FROM test WHERE "
            bind_object = []

            # Add column to be setted
            for key, value in request.get_json().items():
                if key in test_column:
                    print("key:" + key + " exists")
                    delete_sql += "{} = %s AND ".format(key)
                    bind_object.append(value)
                else:
                    return "WARNING key:" + key + " does not exist"
            
            delete_sql = delete_sql[0:-5]

            # Show in logs SQL details
            print("Delete SQL : " + delete_sql)
            print("Bind Object : {}".format(bind_object))
            
            # SQL execution
            cur.execute(delete_sql, tuple(bind_object))
            con.commit()

            # Close communication with the database
            cur.close()
            con.close()
            res = {
                "status": "201",
                "message": "Test {} was deleted successfully".format(request.get_json()["id"])
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

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=3000)
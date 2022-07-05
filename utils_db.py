import psycopg2
import conf

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
        print("Connection failed !")
    
    return con

def insert_test_item(num, data):
    con = None
    try:
        con = get_connection()
        if con is not None:
            cur = con.cursor()  
            cur.execute("INSERT INTO test (num, data, createdAt, updatedAt) VALUES(%s, %s, %s, %s)", (num, data, "NOW()", "NOW()"))
            con.commit()
            print("test itemが正常に追加されました")

            # Close communication with the database
            cur.close()
            con.close()
        else:
            print("connection is None")
    except Exception as error:
        if con is not None:
            con.rollback()
            con.close()
        print("Unexpected Error: {}".format(error))
    
def select_test_item(id):
    con = None
    try:
        con = get_connection() 
        if con is not None:
            cur = con.cursor()
            cur.execute("SELECT * FROM test WHERE id = %s",(id,))
            if cur.fetchone():
                print("test item{}が正常に選択されました".format(id))
            else:
                print("test item{} is None".format(id))
            
            # Close communication with the database
            cur.close()
            con.close()
        else:
            print("connection is None")
    except Exception as error:
        if con is not None:
            con.rollback()
            con.close()
        print("Unexpected Error: {}".format(error))

def update_test_item(id, json_object):
    con = None
    try:
        con = get_connection()
        if con is not None:
            cur = con.cursor()

            # Make sql to update
            update_sql = "UPDATE test SET "
            bind_object = []

            # Add column to be setted
            for key, value in json_object.items():
                if key in test_column:
                    print("key:" + key + " exists")
                    update_sql += "{} = %s, ".format(key)
                    bind_object.append(value)
                else:
                    print("WARNING key:" + key + " does not exist")
            
            update_sql += "updatedAt = NOW()"

            # Add WHERE condition
            update_sql += " WHERE id = %s"
            bind_object.append(id)
            print("Update SQL : " + update_sql)
            print("Bind Object : {}".format(bind_object))
            # print("Bind Object : " + str(bind_object))
            # print("Bind Object :", bind_object)

            cur.execute(update_sql, tuple(bind_object))
            con.commit()
            print("test item{}が正常に更新されました".format(id))
            
            # Close communication with the database
            cur.close()
            con.close()
        else:
            print("connection is None")
    except Exception as error:
        if con is not None:
            con.rollback()
            con.close()
        print("Unexpected Error: {}".format(error))



def delete_test_item(json_object):
    con = None
    try:
        con = get_connection()
        if con is not None:
            cur = con.cursor()
            
            # Execute sql to delete row
            delete_sql = "DELETE FROM test WHERE "
            bind_object = []

            # Add column to be setted
            for key, value in json_object.items():
                if key in test_column:
                    print("key:" + key + " exists")
                    delete_sql += "{} = %s AND ".format(key)
                    bind_object.append(value)
                else:
                    print("WARNING key:" + key + " does not exist")
            
            delete_sql = delete_sql[0:-5]

            # Show in logs SQL details
            print("Delete SQL : " + delete_sql)
            print("Bind Object : {}".format(bind_object))
            
            # SQL execution
            cur.execute(delete_sql, tuple(bind_object))
            con.commit()
            print("test itemが正常に削除されました")

            # Close communication with the database
            cur.close()
            con.close()
        else:
            print("connection is None")
    except Exception as error:
        if con is not None:
            con.rollback()
            con.close()
        print("Unexpected Error: {}".format(error))

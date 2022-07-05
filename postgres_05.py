import psycopg2

#DB接続
def get_connection():
    con = psycopg2.connect( 
        host = "localhost",
        password = "password",
        user = "postgres",
        port = "5432")
    
    #DB接続確認
    if con is not None:
        print("Connection Success !")
    else:
        print("Connection failed !")
    
    return con


def delete(id):
    con = get_connection()
    delete_status = False
    if con is not None:
        try:
            # Open a cursor to perform database operations
            cur = con.cursor()  

            cur.execute("SELECT * FROM test WHERE id = %s", (id,))
            row1 = cur.fetchone()

            if row1 is None:
                cur.close()
                con.close()
                return False
            
            cur.execute("DELETE FROM test WHERE id = %s", (id,))
            con.commit()

            cur.execute("SELECT * FROM test WHERE id = %s", (id,))
            row2 = cur.fetchone()

            # Close communication with the database
            cur.close()
            con.close()

            delete_status = (row2 is None)
        
        except Exception as error:
            con.rollback()
            con.close()
            print("Unexpected Error: {}".format(error))

    return delete_status

if delete(4): #True
    print("Deleted!")

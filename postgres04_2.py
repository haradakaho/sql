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


def update(id):
    con = get_connection()
    update_status = False
    if con is not None:
        try:
            # Open a cursor to perform database operations
            cur = con.cursor()  
            row1 = cur.execute("SELECT updatedAt FROM test WHERE id = %s", (id,))
            row1 = cur.fetchone()

            cur.execute("UPDATE test SET num = 300, updatedAt = NOW() WHERE id = %s", (id,))
            con.commit()

            row2 = cur.execute("SELECT updatedAt FROM test WHERE id = %s", (id,))
            row2 = cur.fetchone()

            # Close communication with the database
            cur.close()
            con.close()

            update_status = (row1[0] != row2[0])

        except Exception as error:
            con.rollback()
            con.close()
            print("Unexpected Error: {}".format(error))

    return update_status

if update(4): #False
    print("Updated!")
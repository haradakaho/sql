import psycopg2

#DB接続
def get_connection():
    con = psycopg2.connect( 
        host = "localhost",
        password = "password",
        user = "postgres",
        port = "5433")
    
    #DB接続確認
    if con is not None:
        print("Connection Success !")
    else:
        print("Connection failed !")
    
    return con


def update(id):
    con = get_connection()
    if con is not None:
        try:
            # Open a cursor to perform database operations
            cur = con.cursor()  

            row1 = cur.execute("SELECT * FROM test WHERE id = %s", (id,))

            row1 = cur.fetchone()
            if row1 is not None:
                print(row1)
                print(row1[1])
            cur.execute("UPDATE test SET num = 100 WHERE id = %s", (id,))
            con.commit()

            row2 = cur.execute("SELECT * FROM test WHERE id = %s", (id,))
            row2 = cur.fetchone()
            if row2 is not None:
                print(row2)
            
            # Close communication with the database
            cur.close()
            con.close()

            if row1[1] == row2[1]:
                return False
            elif row1[1] != row2[1]:
                return True
            else:
                return False
            
        
        except Exception as error:
            con.rollback()
            con.close()
            print("Unexpected Error: {}".format(error))
            return False
if update(2): #False
    print("Updated!")
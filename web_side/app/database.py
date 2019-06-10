import pymysql

class Database:
    def __init__(self):
        host = "35.153.140.109"
        user = "root"
        password = "soylaclavesecreta"
        db = "appdemo"
        port = 3306

        self.con = pymysql.connect(host=host, 
                                    user=user, 
                                    password=password, 
                                    db=db,
                                    port=port)
        try:
            self.cur = self.con.cursor()
        except:
            print('Failed connection.')

    def registerUser(self, username, password, email):
        try:
            
            sql = "INSERT INTO user (username, email, password) VALUES ('{}','{}','{}');".format(username, email, password)
            print(sql)

            self.cur.execute(sql)
            self.con.commit()
            return 'Done'
        except Exception as e:
            print('There is a major problem wht database insert command')
            print(e)
    
    def validUser(self, user, password):
        try:
            sql = "SELECT user_id FROM user WHERE username='{}' AND password='{}'".format(user,password)
            self.cur.execute(sql)
            result = self.cur.fetchone()

            print (result)

            if result == None:
                return False
            else:
                return True

        except Exception as e:
            print('There is a major problem whit database select command')
            print(e)

            return False
        


    def close_connection(self):
        self.cur.close()
        self.con.close()

        return


if __name__ == '__main__':


    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='soylaclavesecreta', db='appdemo')

    cur = conn.cursor()

    cur.execute("INSERT INTO user (username, email, password) VALUES ('diaz','elnigga','asd123');")
    conn.commit()
    cur.execute("select * from user")
    for row in cur:
        print(row)

    cur.close()
    conn.close()
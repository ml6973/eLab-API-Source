import MySQLdb

def initializedb():
    db = MySQLdb.connect(host="129.114.110.223",         # your host, usually localhost
                         user="ubuntu",                  # your username
                         passwd="password",              # your password
                         db="eLabAPI_Brandon")           # name of the data base

    return db

def test():

    db = initializedb()

    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor()

    test = cur.execute("SELECT * FROM Users")

    # print all the first cell of all the rows
    for row in cur.fetchall():
        print row

    db.close()

test()

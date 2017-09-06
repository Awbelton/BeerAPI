import psycopg2

def get_connection():
    conn = psycopg2.connect(host='pellefant.db.elephantsql.com', port='5432', dbname="bliqwaws", user="bliqwaws",
                            password="kkCzkD-1pMEMBqFB-mQnVzOmtWHZ5K3_")
    return conn

def addUser(details):
    # connect to db
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO USERS VALUES(%s, %s, %s)", (details))
    conn.commit()
    conn.close()


def getUsers(details, sel):
    # connect to db
    conn = get_connection()
    cur = conn.cursor()
    if sel == 1:
        cur.execute("SELECT * FROM USERS WHERE id = %s", (details,))
        val = cur.fetchone()
    else:
        cur.execute("SELECT * FROM USERS")
        val = cur.fetchall()
    return val

def getAmt():
    # connect to db
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM USERS")
    val = cur.fetchone()
    return val[0]

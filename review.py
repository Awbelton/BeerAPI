import psycopg2

def get_connection():
    conn = psycopg2.connect(host='pellefant.db.elephantsql.com', port='5432', dbname="bliqwaws", user="bliqwaws",
                            password="kkCzkD-1pMEMBqFB-mQnVzOmtWHZ5K3_")
    return conn

def addReview(details):
    # connect to db
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO REVIEW VALUES(%s, %s, %s, %s, %s, %s, %s)", (details))
    conn.commit()
    conn.close()

def delReview(details):
    # connect to db
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM REVIEW WHERE id = %s", (details,))
    conn.commit()
    conn.close()


def updateReview(details):
    # connect to db
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE REVIEW SET aroma = %s, appearance = %s, taste = %s, overall = %s "
                "WHERE id = %s", details)
    conn.commit()
    conn.close()


def getReviews(details, sel):
    # connect to db
    conn = get_connection()
    cur = conn.cursor()
    if sel == 1:
        cur.execute("SELECT * FROM REVIEW WHERE id = %s", (details,))
        val = cur.fetchone()
    else:
        cur.execute("SELECT * FROM REVIEW")
        val = cur.fetchall()
    return val

def getAmt():
    # connect to db
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM REVIEW")
    val = cur.fetchone()
    return val[0]

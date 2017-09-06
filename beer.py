import psycopg2

def get_connection():
    conn = psycopg2.connect(host='pellefant.db.elephantsql.com', port='5432', dbname="bliqwaws", user="bliqwaws",
                            password="kkCzkD-1pMEMBqFB-mQnVzOmtWHZ5K3_")
    return conn

def addBeer(details):
    # connect to db
    conn = get_connection()
    cur = conn.cursor()
    print(details)
    cur.execute("INSERT INTO BEER VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", details)
    conn.commit()
    conn.close()


def delBeer(details):
    # connect to db
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM BEER WHERE id = %s", (details,))
    conn.commit()
    conn.close()


def updateBeer(details):
    # connect to db
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE BEER SET ibu = %s, calories = %s, abv = %s, brewery = %s, "
                "style = %s WHERE id = %s", details)
    conn.commit()
    conn.close()


def getBeers(details, sel):
    # connect to db
    conn = get_connection()
    cur = conn.cursor()
    if sel == 1:
        cur.execute("SELECT * FROM BEER WHERE id = %s", (details,))
        val = cur.fetchone()
    else:
        cur.execute("SELECT * FROM BEER")
        val = cur.fetchall()
    return val

def getAmt():
    # connect to db
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM BEER")
    val = cur.fetchone()
    return val[0]

def checkAdd(details):
    # connect to db
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM beer WHERE date >= NOW() - '1 day'::INTERVAL AND uid = %s", (details,))
    val = cur.fetchone()

    return val

def getReviews(details):
    # connect to db
    conn = get_connection()
    cur = conn.cursor()

    #TODO : Join on REVIEW table to get beers with reviews
    cur.execute("SELECT review.beerid, review.aroma, review.appearance, review.taste, review.overall, review.userid FROM BEER INNER JOIN REVIEW on beer.id = review.beerid WHERE beer.id = %s", (details, ))
    val = cur.fetchall()
    return val


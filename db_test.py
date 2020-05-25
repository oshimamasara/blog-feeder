import psycopg2

con = psycopg2.connect(host="localhost",database="feed",user="a01",password="Sima58128")
cur = con.cursor()
postgres_insert_query = """ INSERT INTO feed (media, title, url, date) VALUES (%s,%s,%s,%s)"""
record_to_insert = ('yahoo', 'hello_tittle', 'https://', '2020-05-25')
cur.execute(postgres_insert_query, record_to_insert)
con.commit()
cur.close()
con.close()

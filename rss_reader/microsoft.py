# save db OK
import requests
from bs4 import BeautifulSoup
import re
import psycopg2

class MicrosoftObj:
    #def __init__(self, item_counter):
    def __init__(self, loop_counter):
        #print(item_counter)
        res = requests.get('https://devblogs.microsoft.com/')
        soup = BeautifulSoup(res.text, 'html.parser')

        post_title_list = []
        post_url_list = []
        post_date_list = []

        post_titles = soup.find_all('h5', {'class': 'entry-title'})
        for x in post_titles[:3]:
            post_title = x.find('a')
            post_title_list.append(post_title.get_text())

        post_urls = soup.find_all('h5', {'class': 'entry-title'})
        for url in post_urls[:3]:
            post_url = url.find('a')
            post_url_list.append(post_url['href'])

        post_dates = soup.find_all('span',{'class':'entry-post-date'})
        for d in post_dates[:3]:
            post_date = d.get_text()
            post_date_list.append(post_date)

        #print(post_date_list)
        #print(post_url_list)
        #print(post_title_list)


        # db
        media_title = 'Microsoft'
        if loop_counter == 0:
            con = psycopg2.connect(host="localhost",database="feed",user="a01",password="Sima58128")
            cur = con.cursor()
            for t,u,d in zip(post_title_list, post_url_list, post_date_list):
                postgres_insert_query = """ INSERT INTO feed (media, title, url, date) VALUES (%s,%s,%s,%s)"""
                record_to_insert = (media_title, t, u, d)
                cur.execute(postgres_insert_query, record_to_insert)
                con.commit()
                #item_counter += 1

            cur.close()
            con.close()
            print('microsoft!')
        else:
            con = psycopg2.connect(host="localhost",database="feed",user="a01",password="Sima58128")
            cur = con.cursor()
            # 上書きする要素を id から特定
            post_id_list = []
            cur.execute("SELECT id FROM feed WHERE media='Microsoft'")
            rows = cur.fetchall()
            #print(type(rows))  # list
            for i in rows:
                for d in i:  # i は (71,)、keys() は ❌、ループでキーを取得
                    post_id_list.append(d)
                    #print(type(d))  # d = Media:Yahoo の id   , data_type: int


            #print(post_id_list)    #[122, 123, 124]
            for t,u,d,i in zip(post_title_list, post_url_list, post_date_list, post_id_list):
                sql_update_query = """Update feed set title=%s, url=%s, date=%s where id=%s"""
                cur.execute(sql_update_query, (t, u, d, str(i)))
                con.commit()

            cur.close()
            con.close()
            print('microsoft!')

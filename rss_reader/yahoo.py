# save db OK

import requests
from bs4 import BeautifulSoup
import re
import psycopg2

class YahooObj:
    #def __init__(self, item_counter):
    def __init__(self, loop_counter):
        #print(item_counter)
        res = requests.get('https://techblog.yahoo.co.jp/')
        soup = BeautifulSoup(res.text, 'html.parser')
        post_titles = soup.find_all('h3', {'class': 'heading'})

        post_url_list = []
        post_date_list = []
        post_url1 = soup.find("div", class_="panel-horizontal")
        post_url1_1 = post_url1.find('a')['href']
        post_url_list.append(post_url1_1)

        post_date1_1 = post_url1.find("p", class_="date").get_text()
        #print(post_date1_1)
        post_date_list.append(post_date1_1)

        post_urls2 = soup.find_all("div", {'class':'panel-vertical'})
        post_urls2_2 = post_urls2[:2]
        for x in post_urls2_2:
            post_url2_2 = x.find('a')['href']
            post_url_list.append(post_url2_2)
            post_date2_2 = x.find("p", class_="date").get_text()
            post_date_list.append(post_date2_2)
            #print(post_url2)

        #print(post_url_list)   #type--> list
        #print(post_date_list)
        #print(str(post_url))
        #print(post_titles)
        i = 0
        post_title_list = []
        while i < 3:
            post_title = str(post_titles[:3][i])
            post_title = post_title[20:-5]
            post_title_list.append(post_title)
            #print(post_title)
            i += 1
        #print(post_title_list)

        # db
        media_title = 'yahoo'
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
            print('yahoo!')

        else:
            con = psycopg2.connect(host="localhost",database="feed",user="a01",password="Sima58128")
            cur = con.cursor()
            # 上書きする要素を id から特定
            post_id_list = []
            cur.execute("SELECT id FROM feed WHERE media='yahoo'")
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
            print('yahoo!')

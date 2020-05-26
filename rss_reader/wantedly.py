# save db OK
import requests
from bs4 import BeautifulSoup
import re
import psycopg2

class WantedlyObj:
    #def __init__(self, item_counter):
    def __init__(self, loop_counter):
        #print(item_counter)
        res = requests.get('https://www.wantedly.com/feed/s/wantedly_engineers')
        soup = BeautifulSoup(res.text, 'html.parser')

        post_title_list = []
        post_url_list = []
        post_date_list = []

        post_titles = soup.find('div', {'id': 'post-space-infinite-scroll'})
        post_titles = post_titles.find_all('h3',{'class': 'post-title'})
        #print(post_titles)
        for x in post_titles[:3]:
            post_title_list.append(x.get_text()[1:-1])


        post_urls = soup.find('div', {'id': 'post-space-infinite-scroll'})
        post_urls = post_urls.find_all('div', {'class':'post-content'})
        for u in post_urls[:3]:
            post_url = u.find('a')['href']
            post_url_list.append('https://www.wantedly.com' + post_url)  # /companies/wantedly/post_articles/222009

        post_dates = soup.find('div', {'id': 'post-space-infinite-scroll'})
        post_dates = post_dates.find_all('div', {'class':'published_at'})
        for d in post_dates[:3]:
            post_date = d.get_text()[1:-2]
            post_date_list.append(post_date)

        #print(post_title_list)
        #print(post_url_list)
        #print(post_date_list)

        # db
        media_title = 'Wantedly'
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

            print('wantedly!')

        else:
            con = psycopg2.connect(host="localhost",database="feed",user="a01",password="Sima58128")
            cur = con.cursor()
            # 上書きする要素を id から特定
            post_id_list = []
            cur.execute("SELECT id FROM feed WHERE media='Wantedly'")
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
            print('wantedly!')

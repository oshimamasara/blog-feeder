import requests
from bs4 import BeautifulSoup
import re
import psycopg2

class FacebookObj:
    #def __init__(self, item_counter):
    def __init__(self, loop_counter):
        #print(item_counter)
        res = requests.get('https://research.fb.com/blog/')
        soup = BeautifulSoup(res.text, 'html.parser')

        post_title_list = []
        post_url_list = []
        post_date_list = []

        post_titles1 = soup.find('a', {'class': 'featured-post__link'})
        post_title1 = post_titles1.get_text()
        post_title_list.append(post_title1)
        post_titles2 = soup.find_all('a', {'class': 'news-item__link'})
        for x in post_titles2[:2]:
            post_title2 = x.get_text().strip()
            post_title_list.append(post_title2)

        post_urls1 = soup.find('a', {'class': 'featured-post__link'})
        post_url1 = post_urls1['href']
        post_url_list.append(post_url1)
        post_urls2 = soup.find_all('a', {'class': 'news-item__link'})
        for x in post_urls2[:2]:
            post_url2 = x['href']
            post_url_list.append(post_url2)

        post_dates1 = soup.find('p', {'class': 'featured-post__date'})
        post_date1 = post_dates1.get_text()
        post_date_list.append(post_date1)
        post_dates2 = soup.find_all('p', {'class': 'news-item__date'})
        for x in post_dates2[:2]:
            post_date2 = x.get_text()
            post_date_list.append(post_date2)

        #print(post_date_list)
        #print(post_url_list)
        #print(post_title_list)

        # db
        media_title = 'Facebook'
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
            print('Facebook!')

        else:
            con = psycopg2.connect(host="localhost",database="feed",user="a01",password="Sima58128")
            cur = con.cursor()
            # 上書きする要素を id から特定
            post_id_list = []
            cur.execute("SELECT id FROM feed WHERE media='Facebook'")
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
            print('Facebook!')

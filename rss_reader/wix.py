# save db OK
import requests
from bs4 import BeautifulSoup
import re
import psycopg2

class WixObj:
    #def __init__(self, item_counter):
    def __init__(self):
        #print(item_counter)
        res = requests.get('https://www.wix.engineering/blog')
        soup = BeautifulSoup(res.text, 'html.parser')

        post_title_list = []
        post_url_list = []
        post_date_list = []

        post_titles = soup.find_all('a', {'class': 'blog-post-homepage-link-hashtag-hover-color'})
        for x in post_titles[:3]:
            post_title = x.get_text()
            post_title_list.append(post_title)

        post_urls = soup.find_all('a', {'class': 'blog-post-homepage-link-hashtag-hover-color'})
        for x in post_urls[:3]:
            post_url = x['href']
            post_url_list.append(post_url)

        post_dates = soup.find_all('span',{'class':'time-ago'})
        for d in post_dates[:3]:
            post_date = d.get_text()
            post_date_list.append(post_date)

        #print(post_title_list)
        #print(post_url_list)
        #print(post_date_list)


        # db
        media_title = 'Wix'
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

        print('Wix!')

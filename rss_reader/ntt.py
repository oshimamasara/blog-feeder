# 抜けない
import requests
from bs4 import BeautifulSoup
import re
import psycopg2

class NttObj:
    #def __init__(self, item_counter):
    def __init__(self):
        #print(item_counter)
        res = requests.get('https://api.ce-cotoha.com/contents/blog.html')
        soup = BeautifulSoup(res.text, 'html.parser')

        post_title_list = []
        post_url_list = []
        post_date_list = []

        post_titles = soup.find_all('a')
        print(post_titles)

        #print(post_titles)
        #for x in post_titles:
        #    x = x.find('p',{'class': 'un-blog_title'})
        #    post_title_list.append(x.get_text())

        #print(post_title_list)

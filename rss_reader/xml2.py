# データ追加 https://pynative.com/python-postgresql-insert-update-delete-table-data-to-perform-crud-operations/
import feedparser
import psycopg2
import re
import time


class Xml2Obj:
    #def __init__(self, item_counter):
    def __init__(self, loop_counter):
        # １回目のループで insert
        google_url = 'http://feeds.feedburner.com/GDBcode'
        dena_url = 'https://engineer.dena.com/index.xml'
        merukari_url = 'https://tech.mercari.com/feed'
        sakura_url = 'https://knowledge.sakura.ad.jp/rss/' #  published ---> updated あとで処理
        smatrcamp_url = 'https://tech.smartcamp.co.jp/rss'
        salesforce_url = 'https://developer.salesforce.com/jpblogs/feed/'
        asana_url = 'https://blog.asana.com/category/eng/feed/'
        insta_url = 'https://instagram-engineering.com/feed'
        indeed_url = 'https://engineering.indeedblog.com/blog/feed/'
        dropbox_url = 'https://dropbox.tech/feed'
        uber_url = 'https://eng.uber.com/feed/'
        spotify_url = 'https://labs.spotify.com/feed/'

        xml_urls =[google_url,dena_url,merukari_url,sakura_url,smatrcamp_url,salesforce_url,asana_url,insta_url,indeed_url,dropbox_url,uber_url,spotify_url]
        xml_titles =['Google','Dena','Merukari','Sakura','Smatrcamp','SalesForce','Asana','Insta','indeed','DropBox','Uber','Spotify']
        #xml_urls =[google_url,dena_url,merukari_url,sakura_url]

        if loop_counter==0:
            con = psycopg2.connect(host="localhost",database="feed",user="a01",password="Sima58128")
            cur = con.cursor()

            item_id = 0
            for x, t in zip(xml_urls, xml_titles):
                loop_count = 0
                while loop_count < 3:
                    feed_url = feedparser.parse(x)
                    media_title = t
                    print(media_title)
                    post_title = feed_url['entries'][loop_count]['title']
                    post_url = feed_url['entries'][loop_count]['link']
                    if 'published' in feed_url['entries'][loop_count].keys():
                        post_date = feed_url['entries'][loop_count]['published']
                    elif 'updated' in feed_url['entries'][loop_count].keys():
                        post_date = feed_url['entries'][loop_count]['updated']

                    postgres_insert_query = """ INSERT INTO feed (id, media, title, url, date) VALUES (%s,%s,%s,%s,%s)"""
                    record_to_insert = (item_id, media_title, post_title, post_url, post_date)
                    cur.execute(postgres_insert_query, record_to_insert)
                    con.commit()

                    loop_count += 1
                    item_id += 1
            # XML クロール終了

            cur.execute("select id,media,title,url,date from feed")
            for r in cur:
                print(r)

        else:
            # 2回目のループで update
            con = psycopg2.connect(host="localhost",database="feed",user="a01",password="Sima58128")
            cur = con.cursor()

            item_id = 0
            for x, t in zip(xml_urls, xml_titles):
                loop_count = 0
                while loop_count < 3:
                    feed_url = feedparser.parse(x)
                    media_title = t
                    print(media_title)
                    post_title = feed_url['entries'][loop_count]['title']
                    post_url = feed_url['entries'][loop_count]['link']
                    if 'published' in feed_url['entries'][loop_count].keys():
                        post_date = feed_url['entries'][loop_count]['published']
                    elif 'updated' in feed_url['entries'][loop_count].keys():
                        post_date = feed_url['entries'][loop_count]['updated']

                    sql_update_query = """Update feed set title=%s, url=%s, date=%s where id=%s"""
                    cur.execute(sql_update_query, (post_title, post_url, post_date, str(item_id)))
                    con.commit()

                    loop_count += 1
                    item_id += 1

            #cur.execute("select id,media,title,url,date from feed")
            #for r in cur:
            #    print(r)

        cur.close()
        con.close()

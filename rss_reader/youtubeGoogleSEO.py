# save db OK
import requests
import re
from apiclient.discovery import build
import psycopg2

class youtubeGoogleSEOObj:
    #def __init__(self, item_counter):
    def __init__(self, loop_counter):
        #print(item_counter)
        api_key = "AIzaSyBWCirxdCyU9gJM6FmYAHUcOzkghymZ4D0"  # Google Console: sugukesu
        my_youtube = build("youtube","v3",developerKey=api_key)
        request = my_youtube.search().list(
            part="snippet",
            type="video",
            channelId='UCWf2ZlNsCGDS89VBF_awNvA',
            maxResults='3',
            order='date')
        response = request.execute()

        video_title_list = []
        video_url_list = []
        video_img_list = []
        video_date_list = []

        for x in response['items']:
            video_title = x['snippet']['title']
            video_title_list.append(video_title)

        for x in response['items']:
            video_id = x['id']['videoId']
            video_url = 'https://www.youtube.com/watch?v=' + video_id
            video_url_list.append(video_url)

        for x in response['items']:
            video_img = x['snippet']['thumbnails']['high']['url']
            video_img_list.append(video_img)

        for x in response['items']:
            video_date = x['snippet']['publishedAt']
            video_date_list.append(video_date)

        #print(video_title_list)
        #print(video_url_list)
        #print(video_img_list)
        #print(video_date_list)

        # db
        media_title = 'YouTubeGoogleSEO'
        if loop_counter == 0:
            con = psycopg2.connect(host="localhost",database="feed",user="a01",password="Sima58128")
            cur = con.cursor()
            for t,u,d,v in zip(video_title_list, video_url_list, video_date_list, video_img_list):
                postgres_insert_query = """ INSERT INTO feed (media, title, url, date, image) VALUES (%s,%s,%s,%s,%s)"""
                record_to_insert = (media_title, t, u, d, v)
                cur.execute(postgres_insert_query, record_to_insert)
                con.commit()
                #item_counter += 1

            cur.close()
            con.close()
            print('YouTube Google!')

        else:
            con = psycopg2.connect(host="localhost",database="feed",user="a01",password="Sima58128")
            cur = con.cursor()
            # 上書きする要素を id から特定
            post_id_list = []
            cur.execute("SELECT id FROM feed WHERE media='YouTubeGoogleSEO'")
            rows = cur.fetchall()
            #print(type(rows))  # list
            for i in rows:
                for d in i:  # i は (71,)、keys() は ❌、ループでキーを取得
                    post_id_list.append(d)
                    #print(type(d))  # d = Media:Yahoo の id   , data_type: int


            #print(post_id_list)    #[122, 123, 124]
            for t,u,d,v,i in zip(video_title_list, video_url_list, video_date_list, video_img_list, post_id_list):
                sql_update_query = """Update feed set title=%s, url=%s, date=%s, image=%s where id=%s"""
                cur.execute(sql_update_query, (t, u, d, v, str(i)))
                con.commit()

            cur.close()
            con.close()
            print('YouTube Google SEO!')

# save db OK
import requests
import re
from apiclient.discovery import build
import psycopg2

class youtubeGoogleSEOObj:
    #def __init__(self, item_counter):
    def __init__(self):
        #print(item_counter)
        api_key = "AIzaSyCyEUYSaHw5ifFH8kiOyuBQmkqgNO0fkCw"
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
        con = psycopg2.connect(host="localhost",database="feed",user="a01",password="Sima58128")
        cur = con.cursor()
        for t,u,d,i in zip(video_title_list, video_url_list, video_date_list, video_img_list):
            postgres_insert_query = """ INSERT INTO feed (media, title, url, date, image) VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert = (media_title, t, u, d, i)
            cur.execute(postgres_insert_query, record_to_insert)
            con.commit()
            #item_counter += 1

        cur.close()
        con.close()

        print('YouTube Google!')

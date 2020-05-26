from django.shortcuts import render
from django.http import HttpResponse
import feedparser
import psycopg2
import re
# Create your views here.
def myfeed4(request):
    # loop_feed.py で データを DB に保存
    #return HttpResponse("あれ... <a href="">トップにもどる</a> " )

    con = psycopg2.connect(host="localhost",database="feed",user="a01",password="Sima58128")
    cur = con.cursor()
    cur.execute('select distinct media from feed;')
    db_media_title_list = cur.fetchall()  # list > dict   ---> [('instagram-engineering',),
    media_title_list = []
    for i in db_media_title_list:
        for d in i:  # i は dict  ('instagram-engineering',)
            media_title_list.append(d)   # title リスト

    data_dict = {}
    #for t in media_title_list[:1]:
    for t in media_title_list:
        blog_title_list = []
        blog_url_list = []
        blog_media_list = []
        blog_date_list = []
        blog_img_list = []

        select_query = " SELECT title FROM feed WHERE media = %s "
        cur.execute(select_query, (t,))  #data_type:: list -> dict  特定メディアのタイトル３つゲットできた   [('Five things I learned about working on content quality at Instagram',),
        blog_titles = cur.fetchall()
        for bt in blog_titles:
            for b in bt:
                blog_title_list.append(b)
                blog_media_list.append(t)

        select_query = " SELECT url FROM feed WHERE media = %s "
        cur.execute(select_query, (t,))
        blog_urls = cur.fetchall()
        for bu in blog_urls:
            for b in bu:
                blog_url_list.append(b)

        select_query = " SELECT date FROM feed WHERE media = %s "
        cur.execute(select_query, (t,))
        blog_date = cur.fetchall()
        for bd in blog_date:
            for b in bd:
                blog_date_list.append(b)

        select_query = " SELECT image FROM feed WHERE media = %s "
        cur.execute(select_query, (t,))
        blog_image = cur.fetchall()
        for bi in blog_image:
            for b in bi:
                if b == None:
                    blog_img_list.append('')
                else:
                    blog_img_list.append(b)

        #for m, t, u, d, i in zip(blog_media_list, blog_title_list, blog_url_list, blog_date_list, blog_img_list):
        #    print(m + '   ' + t + '   ' + u + '   ' + d + '   ' + i)

        db_data_list = zip(blog_title_list, blog_url_list, blog_date_list, blog_img_list)
        data_dict[t] = db_data_list
    print(data_dict)         # {'instagram-engineering': <zip object at 0x10f747ac8>}
    context = data_dict
    template = 'myfeed/feed4.html'
    return render(request, template, context)
    #return HttpResponse("あれ... <a href="">トップにもどる</a> " )


def myfeed3(request):   #  めちゃ遅い 35s
    google_url = 'http://feeds.feedburner.com/GDBcode'
    dena_url = 'https://engineer.dena.com/index.xml'
    #merukari_url = 'https://tech.mercari.com/feed'
    #sakura_url = 'https://knowledge.sakura.ad.jp/rss/' #  published ---> published
    #smatrcamp_url = 'https://tech.smartcamp.co.jp/rss'
    #salesforce_url = 'https://developer.salesforce.com/jpblogs/feed/'
    #asana_url = 'https://blog.asana.com/category/eng/feed/'
    #insta_url = 'https://instagram-engineering.com/feed'
    #indeed_url = 'https://engineering.indeedblog.com/blog/feed/'
    #dropbox_url = 'https://dropbox.tech/feed'
    #uber_url = 'https://eng.uber.com/feed/'
    #spotify_url = 'https://labs.spotify.com/feed/'

    #xml_urls = [google_url,dena_url,merukari_url,smatrcamp_url,salesforce_url,asana_url,insta_url,indeed_url,dropbox_url,uber_url,spotify_url]
    xml_urls = [google_url,dena_url]
    data_dict = {}
    xml_loop_counter = 0
    for x in xml_urls:
        loop_count = 0
        title_array = []
        link_array = []
        date_array = []
        while loop_count < 3:
            feed_url = feedparser.parse(x)
            title_array.append(feed_url['entries'][loop_count]['title'])
            link_array.append(feed_url['entries'][loop_count]['link'])
            date_array.append(feed_url['entries'][loop_count]['published'])
            loop_count += 1

        list_name = str(xml_loop_counter) + '_data_list'  # google_data_list
        print(list_name)
        list_name_data = zip(title_array, link_array, date_array)
        data_dict[list_name] = list_name_data
        xml_loop_counter += 1
    print(data_dict)
    context = data_dict
    template = 'myfeed/feed3.html'
    return render(request, template, context)




def myfeed2(request):
    google_url = 'http://feeds.feedburner.com/GDBcode'
    dena_url = 'https://engineer.dena.com/index.xml'
    merukari = 'https://tech.mercari.com/feed'
    sakura_url = 'https://knowledge.sakura.ad.jp/rss/' #  published ---> published
    smatrcamp_url = 'https://tech.smartcamp.co.jp/rss'
    salesforce_url = 'https://developer.salesforce.com/jpblogs/feed/'
    asana_url = 'https://blog.asana.com/category/eng/feed/'
    insta_url = 'https://instagram-engineering.com/feed'
    indeed_url = 'https://engineering.indeedblog.com/blog/feed/'
    dropbox_url = 'https://dropbox.tech/feed'
    uber_url = 'https://eng.uber.com/feed/'
    spotify_url = 'https://labs.spotify.com/feed/'

    google_title_array = []
    google_link_array = []
    google_date_array = []
    i = 0
    while i < 3:
        google_feed_url = feedparser.parse(google_url)
        google_title_array.append(google_feed_url['entries'][i]['title'])
        google_link_array.append(google_feed_url['entries'][i]['link'])
        google_date_array.append(google_feed_url['entries'][i]['published'][:10])
        i+=1
    google_data_list = zip(google_title_array, google_link_array, google_date_array)

    context = {'google_data_list':google_data_list}
    template = 'myfeed/feed2.html'
    return render(request, template, context)


    #return HttpResponse("あれ... <a href="">トップにもどる</a> " )
# single test
def myfeed(request):
    #return HttpResponse("あれ... <a href="">トップにもどる</a> " )
    title_array = []
    link_array = []
    date_array = []

    i = 0
    while i < 3:
        feed_url = feedparser.parse("https://timesofindia.indiatimes.com/rssfeedstopstories.cms")
        title_array.append(feed_url['entries'][i]['title'])
        link_array.append(feed_url['entries'][i]['link'])
        date_array.append(feed_url['entries'][i]['published'])
        i+=1

    data_list = zip(title_array, link_array, date_array)
    context = {'data_list':data_list}
    template = 'myfeed/feed.html'
    return render(request, template, context)

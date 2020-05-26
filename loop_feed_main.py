# class tips https://www.youtube.com/watch?v=0v9ATbJTQDc
import time
from rss_reader.xml2 import *
from rss_reader.yahoo import *
from rss_reader.wantedly import *
from rss_reader.fb import *
from rss_reader.microsoft import *
from rss_reader.wix import *
from rss_reader.youtubeGoogleSEO import *


#from rss_reader.ntt import *    # ntt スクレイピング防止している

loop_counter = 0

#yahoo1 = YahooObj(item_counter)

while True:
    yahoo1 = YahooObj(loop_counter)
    wantedly1 = WantedlyObj(loop_counter)
    fb1 = FacebookObj(loop_counter)
    microsoft1 = MicrosoftObj(loop_counter)
    wix1 = WixObj(loop_counter)
    youtubeGoogleSEO = youtubeGoogleSEOObj(loop_counter)

    xml1 = Xml2Obj(loop_counter)

    print('Loop Finish!  回数：' + str(loop_counter))
    loop_counter += 1
    time.sleep(10)



#yahoo1 = yahoo_feed()
#print(yahoo1)

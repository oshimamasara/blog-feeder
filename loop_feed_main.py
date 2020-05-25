# class tips https://www.youtube.com/watch?v=0v9ATbJTQDc
import time
from rss_reader.xml import *
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
    ######yahoo1 = YahooObj()
    ######wantedly1 = WantedlyObj()
    ######fb1 = FacebookObj()
    ######microsoft1 = MicrosoftObj()
    ######wix1 = WixObj()
    ######youtubeGoogleSEO = youtubeGoogleSEOObj()
    xml1 = XmlObj(loop_counter)

    print('Loop Finish!  回数：' + str(loop_counter))
    loop_counter += 1
    time.sleep(10)



#yahoo1 = yahoo_feed()
#print(yahoo1)

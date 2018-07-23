import sys
sys.path.append('C:/Users/Ritvik/Desktop/youTube/')
from youtube_search import youtube_search
import pandas as pd
import json

#non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

test = youtube_search("reflections of light")
"""
video_dict = {'youID':[], 'title':[], 'pub_date':[]}

just_json = test[1]
len(just_json)

i=1
for video in just_json:
    print (i, " : ",video['snippet']['title'].translate(non_bmp_map))
    i=i+1

token = test[0]
youtube_search("spinners", token=token)



video_dict = {'youID':[], 'title':[], 'pub_date':[]}

def grab_videos(keyword, token=None):
    res = youtube_search(keyword, token=token)
    token = res[0]
    videos = res[1]
    for vid in videos:
        video_dict['youID'].append(vid['id']['videoId'])
        video_dict['title'].append(vid['snippet']['title'])
        video_dict['pub_date'].append(vid['snippet']['publishedAt'])
    print ("added " + str(len(videos)) + " videos to a total of " + str(len(video_dict['youID'])))
    return token





token = grab_videos("spinners")
while token != "last_page":
    token = grab_videos("spinners", token=token)
"""

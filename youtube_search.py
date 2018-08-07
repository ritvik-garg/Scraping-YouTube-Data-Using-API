# -*- coding: utf-8 -*-

from apiclient.discovery import build
#from apiclient.errors import HttpError
#from oauth2client.tools import argparser # removed by Dongho
import argparse
import csv
import unidecode
import re

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBBmcr3EQcCe9HA_KtbP_uil8ocKb4iZgI"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

def YTDurationToSeconds(duration):
  match = re.match('PT(\d+H)?(\d+M)?(\d+S)?', duration).groups()
  hours = _js_parseInt(match[0]) if match[0] else 0
  minutes = _js_parseInt(match[1]) if match[1] else 0
  seconds = _js_parseInt(match[2]) if match[2] else 0
  return hours * 3600 + minutes * 60 + seconds

# js-like parseInt
# https://gist.github.com/douglasmiranda/2174255
def _js_parseInt(string):
    return int(''.join([x for x in string if x.isdigit()]))
"""
def get_current_channel_sections(youtube):
  channel_sections_list_response = youtube.channelSections().list(
    part='snippet,contentDetails',
    mine=True,
    
  ).execute()

  return channel_sections_list_response['items']
"""
def youtube_search(q, max_results=50,order="relevance", token=None, location=None, location_radius=None):

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",
    maxResults=max_results,
    location=location,
    locationRadius=location_radius

  ).execute()

  videos = []
  channels = []
  playlists = []
  #comment = []
    
# create a CSV output for video list    
  csvFile = open('video_result.csv','w')
  csvWriter = csv.writer(csvFile)
  csvWriter.writerow(["title","videoId","viewCount","likeCount","dislikeCount","commentCount","favoriteCount","publishedAt","duration","categoryID","caption","license","videoLink","Channel Name","Language"])

  
# Add each result to the appropriate list, and then display the lists of
# matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
      print("hell")
      #print(search_result,'\n\n\n')
      if search_result["id"]["kind"] == "youtube#video":
        #videos.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["videoId"]))
          title = search_result["snippet"]["title"]
          title = unidecode.unidecode(title)  # Dongho 08/10/16
          videoId = search_result["id"]["videoId"]
          #print ('\n\nhaha\n',search_result["contentDetails"]["duration"],'\n\n')
          publishedAt = search_result["snippet"]["publishedAt"]
          #category = search_result["snippet"]["categoryId"]
          
          video_response = youtube.videos().list(id=videoId,part="snippet").execute()
          for video_result in video_response.get("items",[]):
            #print (video_result)
            categoryId = video_result["snippet"]["categoryId"]
            channel_name = video_result["snippet"]["channelTitle"]
            #lang = video_result["snippet"]["localized"]
            #print (channel_name)
            #comment = video_result["snippet"]["topLevelComment"]

          channel_sections = youtube.channelSections().list(part='snippet,contentDetails',mine =True).execute()
          #channel_sections = get_current_channel_sections(youtube)
          
          for channel in channel_sections.get("items",[]):
            print(channel)
            lang = channel_sections["snippet"]["defaultLanguage"]
            print ("haha   ", lang,"\n")
          
          
          #print("title  " , title,"\n")
          link = "https://www.youtube.com/watch?v=" + videoId
          print (title)
          print (link,"\n")
          """
          comment_response = youtube.commentThreads().list(id=videoId, part = "snippet").execute()
          print(videoId,"\n",comment_response)
          
          for item in comment_response["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            print( "Comment by %s: %s" % (author, text))

          #print("hello  \n", comment_response,'\n')
          for comment_result in comment_response.get("items",[]):
            print("hello  ")
            comment = comment_result["snippet"]["topLevelcomment"]
            print ("comment = ", comment,"\n\n")
  
          #print ("comment = ", comment,"\n\n")
          """ 
          video_response = youtube.videos().list(id=videoId,part="status").execute()
          for video_result in video_response.get("items",[]):
            license_ = video_result["status"]["license"]

          video_response = youtube.videos().list(id=videoId,part="contentDetails").execute()
          for video_result in video_response.get("items",[]):
            time = video_result["contentDetails"]["duration"]
            duration = YTDurationToSeconds(time)
            caption = video_result["contentDetails"]["caption"]

          video_response = youtube.videos().list(id=videoId,part="statistics").execute()
          for video_result in video_response.get("items",[]):
              #print("\n\nhaha\n",video_result,'\n\n')
              viewCount = video_result["statistics"]["viewCount"]
              
              if 'likeCount' not in video_result["statistics"]:
                likeCount = 0
              else:
                likeCount = video_result["statistics"]["likeCount"]
              if 'dislikeCount' not in video_result["statistics"]:
                dislikeCount = 0
              else:
                dislikeCount = video_result["statistics"]["dislikeCount"]
              if 'commentCount' not in video_result["statistics"]:
                commentCount = 0
              else:
                commentCount = video_result["statistics"]["commentCount"]
              if 'favoriteCount' not in video_result["statistics"]:
                favoriteCount = 0
              else:
                favoriteCount = video_result["statistics"]["favoriteCount"]

      csvWriter.writerow([title,videoId,viewCount,likeCount,dislikeCount,commentCount,favoriteCount,publishedAt,duration,categoryId,caption,license_,link,channel_name,lang])
  csvFile.close()

      

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search on YouTube')
    parser.add_argument("--q", help="Search term", default="Google")
    parser.add_argument("--max-results", help="Max results", default=25)
    args = parser.parse_args()
    #try:
    youtube_search(args)
    #except HttpError, e:
    #    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

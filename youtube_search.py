# -*- coding: utf-8 -*-

from apiclient.discovery import build
#from apiclient.errors import HttpError
#from oauth2client.tools import argparser # removed by Dongho
import argparse
import csv
import unidecode

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBBmcr3EQcCe9HA_KtbP_uil8ocKb4iZgI"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

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
    
# create a CSV output for video list    
  csvFile = open('video_result.csv','w')
  csvWriter = csv.writer(csvFile)
  csvWriter.writerow(["title","videoId","viewCount","likeCount","dislikeCount","commentCount","favoriteCount","publishedAt","duration","categoryID","caption","license"])

# Add each result to the appropriate list, and then display the lists of
# matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
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
            categoryId = video_result["snippet"]["categoryId"]

          video_response = youtube.videos().list(id=videoId,part="status").execute()
          for video_result in video_response.get("items",[]):
            license_ = video_result["status"]["license"]

          video_response = youtube.videos().list(id=videoId,part="contentDetails").execute()
          for video_result in video_response.get("items",[]):
            duration = video_result["contentDetails"]["duration"]
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
                
          csvWriter.writerow([title,videoId,viewCount,likeCount,dislikeCount,commentCount,favoriteCount,publishedAt,duration,categoryId,caption,license_])

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

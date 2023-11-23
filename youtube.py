import requests
import csv
import os
import time
import json
from datetime import datetime

def read_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data.get('api_key'), data.get('interval_minutes' )

def write_to_csv(file_name, headers, data):
    file_exists = os.path.isfile(file_name)
    
    with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Write headers if file doesn't exist
        if not file_exists:
            writer.writerow(headers)
        
        # Write data
        writer.writerow(data)

def fetch_video_data(video_id, api_key):
    url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={video_id}&key={api_key}"

    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Returns the JSON response if the request was successful
    else:
        return f"Error: {response.status_code}, {response.text}"
    
def parse_video_data(data):

    # Extracting details from the first item in 'items'
    video_info = data["items"][0]

    current_datetime = datetime.now()
    now = current_datetime.isoformat()

    video_id = video_info["id"]
    channel_id = video_info["snippet"]["channelId"]
    channel_title = video_info["snippet"]["channelTitle"]

    title = video_info["snippet"]["title"]

    statistics = video_info["statistics"]
    view_count = statistics["viewCount"]
    like_count = statistics["likeCount"]
    favorite_count = statistics["favoriteCount"]
    comment_count = statistics["commentCount"]


    # Headers and data for CSV
    headers = ["Timestamp", "Channel ID", "Channel Title", "Video ID", "Title", "View Count", "Like Count", "Favorite Count", "Comment Count"]
    data = [now, channel_id, channel_title, video_id, title, view_count, like_count, favorite_count, comment_count]
    print(data)

    return headers, data
    

def fetch_latest_videos(channel_id, api_key, max_results=5):
    # Construct the playlist ID for the channel's uploads
    playlist_id = "UU" + channel_id[2:]

    # URL for the YouTube Data API
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults={max_results}&key={api_key}"

    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Returns the JSON response
    else:
        return f"Error: {response.status_code}, {response.text}"

def parse_latest_videos(data):
    videos = set()    
    for video_info in data["items"]:
        video_id = video_info["snippet"]["resourceId"]["videoId"]
        videos.add(video_id)
    
    return videos


def read_ids(filename):
    ids = set()
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            id = line.strip()
            if id:
                ids.add(id)
    return ids

def save_ids(filename, ids):
    with open(filename, 'w', encoding='utf-8') as file:
        for id in ids:
            file.write(id + '\n')

def infinite_loop():
    api_key, interval_minutes = read_config("config.json")
    file_name = "stats.csv"
    while True:
        video_ids = read_ids("videos.txt")

        channel_ids = read_ids("channels.txt")
        for channel_id in channel_ids:
            data = fetch_latest_videos(channel_id, api_key)
            last_videos = parse_latest_videos(data)
            video_ids = video_ids.union(last_videos)
        
        save_ids("videos.txt", video_ids)
        
        for video_id in video_ids:
            data = fetch_video_data(video_id, api_key)
            headers, row = parse_video_data(data)
            write_to_csv(file_name, headers, row)

        time.sleep(60*interval_minutes)  # Wait for 60 seconds before the next call

infinite_loop()
import traceback
import requests
import csv
import os
import time
import json
from datetime import datetime
import sys

def read_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data.get('api_key'), data.get('interval_minutes'), data.get('start_date')
    
def write_to_csv(file_name, headers, rows):
    file_exists = os.path.isfile(file_name)
    
    with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Write headers if file doesn't exist
        if not file_exists:
            writer.writerow(headers)
        
        # Write data
        for row in rows:
            writer.writerow(row)

def fetch_video_data(video_ids_str, api_key):
    url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={video_ids_str}&key={api_key}"

    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Returns the JSON response if the request was successful
    else:
        return f"Error: {response.status_code}, {response.text}"
    
def parse_video_data(data):

    rows = []
    for video_info in data["items"]:

        current_datetime = datetime.now()
        now = current_datetime.isoformat(timespec='seconds')

        video_id = video_info["id"]
        channel_id = video_info["snippet"]["channelId"]
        channel_title = video_info["snippet"]["channelTitle"]
        liveBroadcastContent = video_info["snippet"]["liveBroadcastContent"]
        publishedAt = video_info["snippet"]["publishedAt"]

        title = video_info["snippet"]["title"]

        statistics = video_info["statistics"]
        view_count = statistics.get("viewCount", 0)  
        like_count = statistics.get("likeCount", 0)  
        favorite_count = statistics.get("favoriteCount", 0) 
        comment_count = statistics.get("commentCount", 0) 

        print(f"{now:<20} {channel_title[:20]:<20} {title[:50]:<50} {view_count:>8} {like_count:>8} {favorite_count:>8} {comment_count:>8}")

        row = [now, channel_id, channel_title, video_id, title, view_count, like_count, favorite_count, comment_count, liveBroadcastContent, publishedAt]
        rows.append(row)

    headers = ["Timestamp", "Channel ID", "Channel Title", "Video ID", "Title", "View Count", "Like Count", "Favorite Count", "Comment Count", "Live Broadcast", "Published"]

    return headers, rows
    

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

def parse_latest_videos(data, start_date):
    
    videos = set()    
    for video_info in data["items"]:
        published_at = video_info["snippet"]["publishedAt"]
        video_id = video_info["snippet"]["resourceId"]["videoId"]
        if published_at > start_date:
            videos.add(video_id)
    
    return videos


def read_ids(filename):
    ids = set()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                id = line.strip().split(' ')[0]
                if id:
                    ids.add(id)
    except:
        pass
    return ids

def save_ids(filename, ids):
    with open(filename, 'w', encoding='utf-8') as file:
        for id in ids:
            file.write(id + '\n')

# Function to divide video_ids into chunks of size n
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def infinite_loop():
    api_key, interval_minutes, start_date = read_config("config.json")
    file_name = "stats.csv"
    while True:
        try:
            video_ids = read_ids("videos.txt")

            channel_ids = read_ids("channels.txt")
            for channel_id in channel_ids:
                data = fetch_latest_videos(channel_id, api_key)
                last_videos = parse_latest_videos(data, start_date)
                video_ids = video_ids.union(last_videos)
            
            save_ids("videos.txt", video_ids)
            
            # Split video_ids into batches of 50
            batch_size = 50
            video_id_batches = list(divide_chunks(list(video_ids), batch_size))

            for batch in video_id_batches:
                # Join IDs in the current batch with a comma
                video_ids_str = ",".join(batch)

                # Fetch and process data for each batch
                data = fetch_video_data(video_ids_str, api_key)
                headers, rows = parse_video_data(data)
                write_to_csv(file_name, headers, rows)

        except Exception:
            traceback.print_exc()

        try:
            time.sleep(60*interval_minutes)  # Wait for 60 seconds before the next call
        except KeyboardInterrupt:
            break

infinite_loop()
import requests

def get_channel_id(api_key, channel_name):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    search_params = {
        "part": "snippet",
        "q": channel_name,
        "type": "channel",
        "key": api_key
    }
    
    response = requests.get(search_url, params=search_params)
    results = response.json()
    
    if "items" in results and len(results["items"]) > 0:
        return results["items"][0]["snippet"]["channelId"]
    else:
        print(f"Channel {channel_name} not found!")
        return None

def get_recent_shorts(api_key, channel_id, max_results=10):
    shorts_url = "https://www.googleapis.com/youtube/v3/search"
    shorts_params = {
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": max_results,
        "order": "date",
        "type": "video",
        "key": api_key
    }
    
    response = requests.get(shorts_url, params=shorts_params)
    results = response.json()

    shorts_data = []
    if "items" in results:
        for item in results["items"]:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            shorts_data.append({"video_id": video_id, "title": title})

    return shorts_data

def get_video_details(api_key, video_ids):
    video_url = "https://www.googleapis.com/youtube/v3/videos"
    video_params = {
        "part": "statistics",
        "id": ",".join(video_ids),
        "key": api_key
    }
    
    response = requests.get(video_url, params=video_params)
    results = response.json()

    video_stats = {}
    if "items" in results:
        for item in results["items"]:
            video_id = item["id"]
            view_count = item["statistics"]["viewCount"]
            video_stats[video_id] = view_count

    return video_stats

def fetch_youtube_data(api_key, channel_name, num_videos):
    channel_id = get_channel_id(api_key, channel_name)
    if channel_id:
        recent_shorts = get_recent_shorts(api_key, channel_id, num_videos)
        video_ids = [short["video_id"] for short in recent_shorts]
        video_details = get_video_details(api_key, video_ids)

        captions = [short["title"] for short in recent_shorts]
        views = [video_details.get(short["video_id"], "N/A") for short in recent_shorts]

        return captions, views
    return [], []

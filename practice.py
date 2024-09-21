from googleapiclient.discovery import build

# Initialize the YouTube API
api_key = "AIzaSyCqSGmhovMVpq8dKmxwo5P4TDKpwRTrrdQ"  
youtube = build('youtube', 'v3', developerKey=api_key)

def search_channels(query, max_results=50):
    """
    Search for channels based on a query and return their statistics.
    """
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="channel",
        maxResults=max_results
    )
    response = request.execute()
    
    channels = []
    
    # Iterate through search results to get channel IDs
    for item in response['items']:
        channel_id = item['snippet']['channelId']
        channel_title = item['snippet']['title']
        # Fetch the channel statistics for each channel
        stats_request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        stats_response = stats_request.execute()
        for channel in stats_response['items']:
            subscribers = int(channel['statistics'].get('subscriberCount', 0))
            views = int(channel['statistics'].get('viewCount', 0))
            channels.append({
                'title': channel_title,
                'id': channel_id,
                'subscribers': subscribers,
                'views': views
            })
    
    return channels

def sort_channels_by_subscribers(channels):
    """
    Sort channels by subscriber count.
    """
    return sorted(channels, key=lambda x: x['subscribers'], reverse=True)

# Search for Somali-related channels
channels = search_channels("Somali")  # You can also try variations like "Somali vlog" or "Somali entertainment"

# Sort the channels by subscribers
top_channels_by_subscribers = sort_channels_by_subscribers(channels)[:10]

# Display the top 10 channels by subscribers
print("Top 10 Somali YouTube Channels by Subscribers:")
for idx, channel in enumerate(top_channels_by_subscribers, start=1):
    print(f"{idx}. {channel['title']} - Subscribers: {channel['subscribers']}, Channel ID: {channel['id']}")

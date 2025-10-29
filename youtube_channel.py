"""
YouTube Channel ID Extractor

This module provides functionality to extract YouTube channel IDs from video URLs or video IDs.
"""

import re
from urllib.parse import urlparse, parse_qs
from typing import Optional

try:
    import requests
except ImportError:
    requests = None


def extract_video_id(url_or_id: str) -> Optional[str]:
    """
    Extract video ID from a YouTube URL or return the ID if it's already a video ID.
    
    Supports various YouTube URL formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID
    - VIDEO_ID (direct video ID)
    
    Args:
        url_or_id: YouTube URL or video ID
        
    Returns:
        Video ID if found, None otherwise
    """
    # If it's already a video ID (11 characters, alphanumeric, dash, underscore)
    if re.match(r'^[A-Za-z0-9_-]{11}$', url_or_id):
        return url_or_id
    
    # Parse URL
    parsed_url = urlparse(url_or_id)
    
    # Handle different YouTube URL formats
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com', 'm.youtube.com']:
        if parsed_url.path == '/watch':
            # Format: https://www.youtube.com/watch?v=VIDEO_ID
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        elif parsed_url.path.startswith('/embed/'):
            # Format: https://www.youtube.com/embed/VIDEO_ID
            return parsed_url.path.split('/')[2]
        elif parsed_url.path.startswith('/v/'):
            # Format: https://www.youtube.com/v/VIDEO_ID
            return parsed_url.path.split('/')[2]
    elif parsed_url.hostname in ['youtu.be']:
        # Format: https://youtu.be/VIDEO_ID
        return parsed_url.path[1:]
    
    return None


def get_channel_id_from_video(url_or_id: str, api_key: Optional[str] = None) -> Optional[str]:
    """
    Get the channel ID for a YouTube video given its URL or video ID.
    
    This function requires a YouTube Data API v3 key to function.
    You can get one from: https://console.developers.google.com/
    
    Args:
        url_or_id: YouTube video URL or video ID
        api_key: YouTube Data API v3 key
        
    Returns:
        Channel ID if found, None otherwise
        
    Raises:
        ValueError: If no API key is provided
        requests.exceptions.RequestException: If the API request fails
    """
    if not api_key:
        raise ValueError("YouTube Data API key is required. Get one from https://console.developers.google.com/")
    
    # Extract video ID
    video_id = extract_video_id(url_or_id)
    if not video_id:
        return None
    
    # Check if requests is available
    if requests is None:
        raise ImportError("requests library is required. Install it with: pip install requests")
    
    # Call YouTube Data API
    api_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        'part': 'snippet',
        'id': video_id,
        'key': api_key
    }
    
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    # Extract channel ID from response
    if 'items' in data and len(data['items']) > 0:
        return data['items'][0]['snippet']['channelId']
    
    return None


def get_channel_id_from_video_no_api(url_or_id: str) -> Optional[str]:
    """
    Get the channel ID for a YouTube video without using the API (web scraping).
    
    This is a fallback method that scrapes the YouTube page. It's less reliable
    than using the API but doesn't require an API key.
    
    Args:
        url_or_id: YouTube video URL or video ID
        
    Returns:
        Channel ID if found, None otherwise
    """
    # Extract video ID
    video_id = extract_video_id(url_or_id)
    if not video_id:
        return None
    
    # Check if requests is available
    if requests is None:
        raise ImportError("requests library is required. Install it with: pip install requests")
    
    # Fetch the video page
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    response = requests.get(video_url)
    response.raise_for_status()
    
    # Search for channel ID in the page
    # YouTube includes channel ID in various places in the page source
    channel_id_pattern = r'"channelId":"([A-Za-z0-9_-]+)"'
    match = re.search(channel_id_pattern, response.text)
    
    if match:
        return match.group(1)
    
    # Alternative pattern
    alt_pattern = r'"browseId":"([A-Za-z0-9_-]+)"'
    match = re.search(alt_pattern, response.text)
    
    if match:
        channel_id = match.group(1)
        # Browse IDs for channels start with UC
        if channel_id.startswith('UC'):
            return channel_id
    
    return None


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python youtube_channel.py <youtube_url_or_video_id> [api_key]")
        print("\nExamples:")
        print("  python youtube_channel.py 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'")
        print("  python youtube_channel.py 'dQw4w9WgXcQ' YOUR_API_KEY")
        sys.exit(1)
    
    url_or_id = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) > 2 else None
    
    # First, just extract the video ID
    video_id = extract_video_id(url_or_id)
    print(f"Video ID: {video_id}")
    
    # Try to get channel ID
    if api_key:
        try:
            channel_id = get_channel_id_from_video(url_or_id, api_key)
            print(f"Channel ID (via API): {channel_id}")
        except Exception as e:
            print(f"Error using API: {e}")
    else:
        print("\nNo API key provided. Trying web scraping method...")
        try:
            channel_id = get_channel_id_from_video_no_api(url_or_id)
            print(f"Channel ID (via web scraping): {channel_id}")
        except Exception as e:
            print(f"Error using web scraping: {e}")

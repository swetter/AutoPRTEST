#!/usr/bin/env python3
"""
Example script demonstrating how to use the YouTube channel ID extractor
"""

from youtube_channel import extract_video_id, get_channel_id_from_video, get_channel_id_from_video_no_api


def example_1_extract_video_id():
    """Example: Extract video ID from various URL formats"""
    print("=" * 60)
    print("Example 1: Extract Video ID from Various URLs")
    print("=" * 60)
    
    urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "dQw4w9WgXcQ",
    ]
    
    for url in urls:
        video_id = extract_video_id(url)
        print(f"URL: {url}")
        print(f"Video ID: {video_id}\n")


def example_2_get_channel_id_with_api():
    """Example: Get channel ID using YouTube API"""
    print("=" * 60)
    print("Example 2: Get Channel ID Using YouTube API")
    print("=" * 60)
    
    # NOTE: You need to replace 'YOUR_API_KEY' with an actual YouTube Data API key
    # Get one from: https://console.developers.google.com/
    
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    
    print(f"Video URL: {video_url}")
    print(f"API Key: {'*' * len(api_key) if api_key != 'YOUR_API_KEY' else 'Not set'}")
    
    if api_key == "YOUR_API_KEY":
        print("\nNote: You need to set a real API key to use this example")
        print("Get one from: https://console.developers.google.com/")
    else:
        try:
            channel_id = get_channel_id_from_video(video_url, api_key)
            print(f"Channel ID: {channel_id}")
        except Exception as e:
            print(f"Error: {e}")
    
    print()


def example_3_get_channel_id_without_api():
    """Example: Get channel ID using web scraping (no API key required)"""
    print("=" * 60)
    print("Example 3: Get Channel ID Without API (Web Scraping)")
    print("=" * 60)
    
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"Video URL: {video_url}")
    print("Note: This method scrapes the YouTube page and may be less reliable")
    
    try:
        channel_id = get_channel_id_from_video_no_api(video_url)
        print(f"Channel ID: {channel_id}")
    except Exception as e:
        print(f"Error: {e}")
    
    print()


def example_4_batch_processing():
    """Example: Process multiple videos"""
    print("=" * 60)
    print("Example 4: Batch Process Multiple Videos")
    print("=" * 60)
    
    video_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/9bZkp7q19f0",
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",
    ]
    
    print("Extracting video IDs from multiple URLs:")
    for url in video_urls:
        video_id = extract_video_id(url)
        print(f"  {url[:50]:50} -> {video_id}")
    
    print()


if __name__ == "__main__":
    print("\nYouTube Channel ID Extractor - Examples\n")
    
    # Run all examples
    example_1_extract_video_id()
    example_2_get_channel_id_with_api()
    example_3_get_channel_id_without_api()
    example_4_batch_processing()
    
    print("=" * 60)
    print("For more information, see README.md")
    print("=" * 60)

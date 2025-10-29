# AutoPRTEST

YouTube Channel ID Extractor - A Python utility to extract YouTube channel IDs from video URLs or video IDs.

## Features

- Extract video IDs from various YouTube URL formats
- Get channel ID using YouTube Data API v3
- Fallback web scraping method when API key is not available
- Support for multiple YouTube URL formats:
  - `https://www.youtube.com/watch?v=VIDEO_ID`
  - `https://youtu.be/VIDEO_ID`
  - `https://www.youtube.com/embed/VIDEO_ID`
  - `https://www.youtube.com/v/VIDEO_ID`
  - Direct video ID

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### As a Python Module

```python
from youtube_channel import extract_video_id, get_channel_id_from_video, get_channel_id_from_video_no_api

# Extract video ID from URL
video_id = extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(f"Video ID: {video_id}")

# Get channel ID using YouTube API (requires API key)
api_key = "YOUR_YOUTUBE_API_KEY"
channel_id = get_channel_id_from_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", api_key)
print(f"Channel ID: {channel_id}")

# Get channel ID without API (web scraping - less reliable)
channel_id = get_channel_id_from_video_no_api("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(f"Channel ID: {channel_id}")
```

### Command Line

```bash
# Without API key (uses web scraping)
python youtube_channel.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# With API key
python youtube_channel.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" YOUR_API_KEY

# Using just video ID
python youtube_channel.py "dQw4w9WgXcQ"
```

## Getting a YouTube API Key

To use the API method, you need a YouTube Data API v3 key:

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API key)
5. Use the API key in your code

## Running Tests

```bash
python -m unittest test_youtube_channel.py
```

## API vs Web Scraping

### YouTube Data API v3 (Recommended)
- **Pros**: Reliable, official, structured data
- **Cons**: Requires API key, has quota limits

### Web Scraping (Fallback)
- **Pros**: No API key required, no quota limits
- **Cons**: Less reliable, may break if YouTube changes their HTML structure

## License

MIT
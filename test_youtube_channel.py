"""
Tests for YouTube channel ID extraction functionality
"""

import unittest
from unittest.mock import patch, Mock
from youtube_channel import extract_video_id, get_channel_id_from_video, get_channel_id_from_video_no_api


class TestExtractVideoId(unittest.TestCase):
    """Test cases for extract_video_id function"""
    
    def test_direct_video_id(self):
        """Test with a direct video ID"""
        video_id = "dQw4w9WgXcQ"
        result = extract_video_id(video_id)
        self.assertEqual(result, video_id)
    
    def test_watch_url(self):
        """Test with youtube.com/watch URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = extract_video_id(url)
        self.assertEqual(result, "dQw4w9WgXcQ")
    
    def test_watch_url_with_params(self):
        """Test with youtube.com/watch URL with additional parameters"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s"
        result = extract_video_id(url)
        self.assertEqual(result, "dQw4w9WgXcQ")
    
    def test_short_url(self):
        """Test with youtu.be short URL"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        result = extract_video_id(url)
        self.assertEqual(result, "dQw4w9WgXcQ")
    
    def test_embed_url(self):
        """Test with youtube.com/embed URL"""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        result = extract_video_id(url)
        self.assertEqual(result, "dQw4w9WgXcQ")
    
    def test_v_url(self):
        """Test with youtube.com/v URL"""
        url = "https://www.youtube.com/v/dQw4w9WgXcQ"
        result = extract_video_id(url)
        self.assertEqual(result, "dQw4w9WgXcQ")
    
    def test_mobile_url(self):
        """Test with m.youtube.com URL"""
        url = "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
        result = extract_video_id(url)
        self.assertEqual(result, "dQw4w9WgXcQ")
    
    def test_invalid_url(self):
        """Test with invalid URL"""
        url = "https://www.google.com"
        result = extract_video_id(url)
        self.assertIsNone(result)
    
    def test_invalid_video_id(self):
        """Test with invalid video ID format"""
        video_id = "invalid"
        result = extract_video_id(video_id)
        self.assertIsNone(result)


class TestGetChannelIdFromVideo(unittest.TestCase):
    """Test cases for get_channel_id_from_video function"""
    
    def test_no_api_key(self):
        """Test that ValueError is raised when no API key is provided"""
        with self.assertRaises(ValueError):
            get_channel_id_from_video("dQw4w9WgXcQ", api_key=None)
    
    @patch('youtube_channel.requests.get')
    def test_successful_api_call(self, mock_get):
        """Test successful API call to get channel ID"""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [
                {
                    'snippet': {
                        'channelId': 'UCuAXFkgsw1L7xaCfnd5JJOw'
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_channel_id_from_video("dQw4w9WgXcQ", api_key="fake_api_key")
        self.assertEqual(result, "UCuAXFkgsw1L7xaCfnd5JJOw")
        
        # Verify API was called correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertEqual(call_args[0][0], "https://www.googleapis.com/youtube/v3/videos")
        self.assertEqual(call_args[1]['params']['id'], "dQw4w9WgXcQ")
        self.assertEqual(call_args[1]['params']['key'], "fake_api_key")
    
    @patch('youtube_channel.requests.get')
    def test_api_call_with_url(self, mock_get):
        """Test API call with a full URL instead of video ID"""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [
                {
                    'snippet': {
                        'channelId': 'UCuAXFkgsw1L7xaCfnd5JJOw'
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_channel_id_from_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", api_key="fake_api_key")
        self.assertEqual(result, "UCuAXFkgsw1L7xaCfnd5JJOw")
    
    @patch('youtube_channel.requests.get')
    def test_api_call_no_results(self, mock_get):
        """Test API call when video doesn't exist"""
        # Mock API response with no items
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_channel_id_from_video("dQw4w9WgXcQ", api_key="fake_api_key")
        self.assertIsNone(result)
    
    def test_invalid_video_id(self):
        """Test with invalid video ID"""
        result = get_channel_id_from_video("invalid", api_key="fake_api_key")
        self.assertIsNone(result)


class TestGetChannelIdFromVideoNoApi(unittest.TestCase):
    """Test cases for get_channel_id_from_video_no_api function"""
    
    @patch('youtube_channel.requests.get')
    def test_successful_scraping(self, mock_get):
        """Test successful web scraping to get channel ID"""
        # Mock HTML response
        mock_response = Mock()
        mock_response.text = '''
        <html>
            <script>
                var ytInitialData = {"channelId":"UCuAXFkgsw1L7xaCfnd5JJOw"};
            </script>
        </html>
        '''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_channel_id_from_video_no_api("dQw4w9WgXcQ")
        self.assertEqual(result, "UCuAXFkgsw1L7xaCfnd5JJOw")
    
    @patch('youtube_channel.requests.get')
    def test_scraping_with_browse_id(self, mock_get):
        """Test web scraping with browseId pattern"""
        # Mock HTML response with browseId
        mock_response = Mock()
        mock_response.text = '''
        <html>
            <script>
                var ytInitialData = {"browseId":"UCuAXFkgsw1L7xaCfnd5JJOw"};
            </script>
        </html>
        '''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_channel_id_from_video_no_api("dQw4w9WgXcQ")
        self.assertEqual(result, "UCuAXFkgsw1L7xaCfnd5JJOw")
    
    @patch('youtube_channel.requests.get')
    def test_scraping_no_channel_id_found(self, mock_get):
        """Test web scraping when channel ID is not found"""
        # Mock HTML response without channel ID
        mock_response = Mock()
        mock_response.text = '<html><body>No channel ID here</body></html>'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_channel_id_from_video_no_api("dQw4w9WgXcQ")
        self.assertIsNone(result)
    
    @patch('youtube_channel.requests.get')
    def test_scraping_with_url(self, mock_get):
        """Test web scraping with a full URL"""
        # Mock HTML response
        mock_response = Mock()
        mock_response.text = '''
        <html>
            <script>
                var ytInitialData = {"channelId":"UCuAXFkgsw1L7xaCfnd5JJOw"};
            </script>
        </html>
        '''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_channel_id_from_video_no_api("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertEqual(result, "UCuAXFkgsw1L7xaCfnd5JJOw")
    
    def test_invalid_video_id(self):
        """Test with invalid video ID"""
        result = get_channel_id_from_video_no_api("invalid")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

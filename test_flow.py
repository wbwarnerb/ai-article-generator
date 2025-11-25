import unittest
from unittest.mock import patch, MagicMock
from scraper import fetch_headlines
from generator import generate_story
from publisher import publish_to_wordpress

class TestGravityStorybuilder(unittest.TestCase):

    @patch('scraper.feedparser.parse')
    def test_fetch_headlines(self, mock_parse):
        # Mock feedparser response
        mock_feed = MagicMock()
        mock_feed.bozo = 0
        mock_entry = MagicMock()
        mock_entry.title = "Test Headline"
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed
        
        headlines = fetch_headlines(["http://test.com/rss"])
        self.assertEqual(headlines, ["Test Headline"])
        
    @patch('generator.OpenAI')
    @patch.dict('os.environ', {'AI_API_KEY': 'test_key'})
    def test_generate_story(self, mock_openai):
        # Mock OpenAI response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "TITLE: New Title\nCONTENT: Generated Story Content"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        title, content = generate_story("Headline 1", "positive")
        self.assertEqual(title, "New Title")
        self.assertEqual(content, "Generated Story Content")
        
    @patch('publisher.requests.post')
    @patch.dict('os.environ', {'WP_URL': 'http://wp.com', 'WP_USER': 'user', 'WP_APP_PASSWORD': 'pass'})
    def test_publish_to_wordpress(self, mock_post):
        # Mock requests response
        mock_response = MagicMock()
        mock_response.json.return_value = {'link': 'http://wp.com/post/1'}
        mock_post.return_value = mock_response
        
        result = publish_to_wordpress("Title", "Content")
        self.assertIn("Successfully published", result)
        self.assertIn("http://wp.com/post/1", result)

if __name__ == '__main__':
    unittest.main()

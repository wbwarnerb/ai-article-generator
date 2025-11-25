import unittest
from unittest.mock import patch, MagicMock
from generator import generate_story
from publisher import publish_to_wordpress
from personalities import PERSONALITIES

class TestPersonalities(unittest.TestCase):

    @patch('generator.OpenAI')
    @patch('os.getenv')
    def test_generate_story_uses_personality_context(self, mock_getenv, mock_openai):
        mock_getenv.return_value = "fake_key"
        
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "TITLE: Test Title\nCONTENT: Test Content"
        mock_client.chat.completions.create.return_value = mock_response
        
        headline = "Test Headline"
        personality_context = "Be funny."
        
        generate_story(headline, personality_context)
        
        # Check if the personality context was passed in the prompt
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args[1]['messages']
        user_prompt = messages[1]['content']
        
        self.assertIn(personality_context, user_prompt)

    @patch('publisher.requests.post')
    @patch('os.getenv')
    def test_publish_to_wordpress_uses_credentials(self, mock_getenv, mock_post):
        mock_getenv.return_value = "https://example.com" # for WP_URL
        
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {'link': 'http://example.com/post'}
        
        title = "Test Title"
        content = "Test Content"
        wp_user = "test_user"
        wp_pass = "test_pass"
        
        publish_to_wordpress(title, content, wp_user, wp_pass)
        
        # Check if credentials were used in the auth header
        call_args = mock_post.call_args
        headers = call_args[1]['headers']
        auth_header = headers['Authorization']
        
        # Base64 encode "test_user:test_pass" -> "dGVzdF91c2VyOnRlc3RfcGFzcw=="
        expected_token = "dGVzdF91c2VyOnRlc3RfcGFzcw=="
        self.assertIn(expected_token, auth_header)

if __name__ == '__main__':
    unittest.main()

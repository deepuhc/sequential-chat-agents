"""
test_recommender.py

This module contains unit tests for the sequential-chat-agents project.
It tests agent creation, chat configuration loading, and recommendation logic.
"""
import unittest
from unittest.mock import patch, MagicMock
import yaml
from src.recommender import RecommendationManager
from src.agents import create_agents

class TestRecommendationSystem(unittest.TestCase):
    """Test suite for the recommendation system."""

    @patch('src.utils.get_gemini_api_key')
    def test_create_agents(self, mock_get_api_key):
        """Test that agents are created with correct configurations."""
        mock_get_api_key.return_value = "test_gemini_key"
        agents = create_agents()
        self.assertEqual(len(agents), 4)
        self.assertEqual(agents[0].name, "UserInfoAgent")
        self.assertEqual(agents[1].name, "PreferenceAgent")
        self.assertEqual(agents[2].name, "RecommendationAgent")
        self.assertEqual(agents[3].name, "UserProxy")

    @patch('src.recommender.yaml.safe_load')
    @patch('builtins.open')
    def test_load_chat_configs(self, mock_open, mock_yaml_load):
        """Test that chat configurations are loaded correctly."""
        mock_yaml_load.return_value = {
            "chats": {
                "user_info": {
                    "message": "Hello!",
                    "summary_prompt": "Summarize user info."
                },
                "preferences": {
                    "message": "Preferences?",
                    "summary_prompt": "Summarize preferences."
                },
                "recommendation": {
                    "message": "Recommend!",
                    "summary_prompt": "Summarize recommendations."
                }
            }
        }
        manager = RecommendationManager(config_path="dummy_config.yaml")
        self.assertEqual(len(manager.chat_configs), 3)
        self.assertEqual(manager.chat_configs[0]["message"], "Hello!")
        self.assertEqual(manager.chat_configs[0]["summary_method"], "last_msg")

    @patch('src.recommender.yaml.safe_load')
    @patch('builtins.open')
    def test_missing_config_file(self, mock_open, mock_yaml_load):
        """Test error handling for missing config file."""
        mock_open.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            RecommendationManager(config_path="nonexistent.yaml")

    @patch('src.recommender.initiate_chats')
    @patch('src.utils.get_gemini_api_key')
    def test_run_chats(self, mock_get_api_key, mock_initiate_chats):
        """Test that chats are executed correctly."""
        mock_get_api_key.return_value = "test_gemini_key"
        mock_result = MagicMock(summary="Test summary", cost={"total_cost": 0.0})
        mock_initiate_chats.return_value = [mock_result]
        manager = RecommendationManager()
        results = manager.run_chats()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].summary, "Test summary")

if __name__ == '__main__':
    unittest.main()
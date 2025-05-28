"""
recommender.py

This module implements a sequential chat system using AutoGen to recommend movies
and songs based on user input (location, introduction, preferences). It supports
YAML configuration, error handling, and retry logic for production use.

Usage:
    Run `python src/recommender.py` to start the recommendation process.
"""
import yaml
import sys
import os
from typing import List, Dict, Any
from autogen import initiate_chats
from src.agents import create_agents
import backoff

# Ensure project root is in Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class RecommendationManager:
    """Manages sequential chat for movie and song recommendations."""
    
    def __init__(self, config_path: str = "configs/config.yaml"):
        """
        Initialize with configuration from a YAML file.

        Args:
            config_path (str): Path to YAML configuration file.
        """
        self.config_path = config_path
        self.agents = create_agents()
        self.chat_configs = self._load_chat_configs()
        
    def _load_chat_configs(self) -> List[Dict[str, Any]]:
        """
        Load chat configurations from YAML file.

        Returns:
            List[Dict[str, Any]]: List of chat configurations.

        Raises:
            FileNotFoundError: If config file is missing.
            yaml.YAMLError: If YAML is invalid.
        """
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file {self.config_path} not found")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing {self.config_path}: {e}")

        user_info_agent, preference_agent, recommendation_agent, user_proxy = self.agents

        return [
            {
                "sender": user_info_agent,
                "recipient": user_proxy,
                "message": config["chats"]["user_info"]["message"],
                "summary_method": "last_msg",  # Changed to avoid reflection_with_llm issues
                "max_turns": 2,
                "clear_history": True
            },
            {
                "sender": preference_agent,
                "recipient": user_proxy,
                "message": config["chats"]["preferences"]["message"],
                "summary_method": "last_msg",
                "max_turns": 2,
                "clear_history": False
            },
            {
                "sender": user_proxy,
                "recipient": recommendation_agent,
                "message": config["chats"]["recommendation"]["message"],
                "summary_method": "last_msg",
                "max_turns": 1,
                "clear_history": False
            }
        ]

    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    def run_chats(self) -> List[Any]:
        """
        Execute the sequential chat process.

        Returns:
            List[Any]: List of chat results.

        Raises:
            Exception: If chat execution fails after retries.
        """
        try:
            chat_results = initiate_chats(self.chat_configs)
            return chat_results
        except Exception as e:
            print(f"Chat execution failed: {e}")
            raise

def main():
    """Main function to run the recommendation system."""
    try:
        manager = RecommendationManager()
        chat_results = manager.run_chats()

        print("=== Recommendation Summary ===")
        for i, result in enumerate(chat_results, 1):
            # Safely extract summary, handling potential dict
            summary = result.summary
            if isinstance(summary, dict):
                summary = summary.get("content", "No summary available")
            print(f"\nChat {i} Summary:\n{summary}")
            print(f"\nChat {i} Cost:\n{result.cost}")

    except Exception as e:
        print(f"Error running recommendation system: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
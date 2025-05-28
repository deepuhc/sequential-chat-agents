"""
agents.py

This module defines AutoGen ConversableAgent instances for the sequential chat
recommendation system. Agents collect user information and provide movie and song
recommendations based on user preferences.
"""
from autogen import ConversableAgent
from src.utils import get_gemini_api_key

def create_agents() -> tuple:
    """
    Creates and configures agents for user data collection and recommendations.

    Returns:
        tuple: (user_info_agent, preference_agent, recommendation_agent, user_proxy)
    """
    api_key = get_gemini_api_key()
    llm_config = {
        "model": "gemini-1.5-flash",
        "api_key": api_key,
        "api_type": "google",
        "max_tokens": 100
    }

    user_info_agent = ConversableAgent(
        name="UserInfoAgent",
        system_message="""You are a friendly assistant collecting user information.
        Ask for the user's name, location, and a brief introduction about themselves.
        Do not ask for other details. Return 'TERMINATE' when done.""",
        llm_config=llm_config,
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: "terminate" in msg.get("content", "").lower()
    )

    preference_agent = ConversableAgent(
        name="PreferenceAgent",
        system_message="""You are a friendly assistant collecting user preferences.
        Ask for the user's favorite movie genres and music preferences (e.g., genres, artists).
        Do not ask for other details. Return 'TERMINATE' when done.""",
        llm_config=llm_config,
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: "terminate" in msg.get("content", "").lower()
    )

    recommendation_agent = ConversableAgent(
        name="RecommendationAgent",
        system_message="""You are an expert recommender providing personalized movie and song suggestions.
        Use the user's location, introduction, movie genres, and music preferences to suggest:
        - 2 movies with titles and brief reasons.
        - 2 songs with titles, artists, and brief reasons.
        Make it engaging and tailored! Return 'TERMINATE' when done.""",
        llm_config=llm_config,
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: "terminate" in msg.get("content", "").lower()
    )

    user_proxy = ConversableAgent(
        name="UserProxy",
        llm_config=False,
        code_execution_config=False,
        human_input_mode="ALWAYS",
        is_termination_msg=lambda msg: "terminate" in msg.get("content", "").lower()
    )

    return user_info_agent, preference_agent, recommendation_agent, user_proxy
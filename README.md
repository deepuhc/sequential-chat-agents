Sequential Chat Agents: Movie & Song Recommender
Welcome to the Sequential Chat Agents project, a Python application powered by AutoGen and Google's Gemini API. It delivers personalized movie and song recommendations through a sequential chat design, collecting user details like name, location, introduction, and preferences (movie genres, music tastes). Designed for modularity and robustness, it’s ideal for AI-driven recommendation systems and is production-ready with comprehensive tests and documentation.
Features

Sequential Chat Workflow: Engages users step-by-step to gather information and provide tailored recommendations.
Personalized Suggestions: Recommends movies and songs based on user location, introduction, and preferences.
Configurable Design: Uses YAML for customizable chat messages and prompts.
Robust Error Handling: Includes retry logic and input validation for reliability.
Unit Tests: Ensures code quality with comprehensive test coverage.
Professional Structure: Organized with src/, tests/, and configs/ directories.

Prerequisites

Python: 3.10.13
Gemini API Key: Obtain from Google's API Console
Dependencies: Listed in requirements.txt

Installation

Clone the Repository:
git clone https://github.com/deepuhc/sequential-chat-agents.git
cd sequential-chat-agents


Set Up Python 3.10.13:
brew install pyenv
pyenv install 3.10.13
pyenv global 3.10.13
python3 --version


Create and Activate Virtual Environment:
python3 -m venv venv
source venv/bin/activate


Install Dependencies:
pip install -r requirements.txt


Configure Gemini API Key:Add to ~/.env:
echo 'GEMINI_API_KEY=your_gemini_api_key' >> ~/.env



Usage
Run the recommender:
python src/recommender.py


Follow Prompts: Enter your name, location, introduction, and preferences (movie genres, music tastes).
Receive Recommendations: Get two movie and two song suggestions tailored to your input.
Example Output:=== Recommendation Summary ===
Chat 1 Summary:
User is Alice from New York, a student who loves adventure.

Chat 2 Summary:
Alice prefers action movies and pop music.

Chat 3 Summary:
Recommended: 'Inception' (action-packed thriller), 'Mad Max: Fury Road' (high-energy action); 'Shape of You' by Ed Sheeran (pop hit), 'Dancing Queen' by ABBA (classic pop).



Run tests:
python -m unittest tests/test_recommender.py -v

Project Structure
sequential-chat-agents/
├── src/
│   ├── agents.py         # Agent definitions
│   ├── recommender.py    # Sequential chat logic
│   └── utils.py          # Utility functions
├── tests/
│   └── test_recommender.py  # Unit tests
├── configs/
│   └── config.yaml       # Chat configurations
├── requirements.txt      # Dependencies
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
├── README.md             # This file

Configuration
Customize chat messages in configs/config.yaml:
chats:
  user_info:
    message: "Hello! Could you tell me your name, location, and a brief introduction?"

Contributing

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
MIT License. See LICENSE for details.
Acknowledgments

Built with AutoGen.
Powered by Google's Gemini API.


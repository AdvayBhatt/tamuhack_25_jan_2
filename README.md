# tamuhack_25_jan
A Financial Advisor chatbot that helps users manage their funds and tracks future investments. 

## How You Can Use Coinvo

As there is not a deployed website yet, to run Coinvo, follow this:
1. Make sure you have the Python packages flask, streamlit, openai, json, pandas, matplotlib, yfinance, os, requests, webbrowser, fastapi, uvicorn, subprocess
    - to install, make sure you have downloaded pip and then 'pip install' these packages listed above. It may only work when you do 'pip install' one package at a time.
2. Assuming you are seeing the repository on GitHub, go to a terminal and input 'git clone https://github.com/AdvayBhatt/tamuhack_25_jan_2.git' in a folder you would like this repository to show up in on your local machine
3. If you are using VS Code, make sure you have the Live Server extension downloaded to run the website
4. Open up a terminal, cd to the directory where you have cloned the repo, then input 'uvicorn backend:app --reload'
5. Open a new terminal and run 'python app.py' (make sure you are in the same directory)
6. Open another new terminal and run 'streamlit run main.py' (again make sure you are in the right directory)
7. This will automatically open the chatbot but to access the main website page, open index.html and if you are using VS Code, click Go Live in the bottom right corner

Enjoy the website!

## Inspiration

In a world flooded with financial tools, we often found ourselves overwhelmed of where to turn for clear, actionable insights. That feeling inspired us to create Coinvo, a platform that combines real-time stock tracking with the guidance of an AI-powered assistant. Coinvo bridges the gap between data and understanding, empowering everyone from casual investors to financial enthusiasts to make informed decisions.
## What it does
Coinvo is your personal financial co-pilot. It integrates a stock ticker for real-time market data and an AI helper bot that answers questions, offers insights, and provides context on financial topics. Whether you're analyzing stock performance, seeking investment strategies, or simply curious about the market, Coinvo is here to make finance approachable and actionable.

## How we built it
Backend: Flask to manage routes and serve dynamic content.
Frontend: HTML, CSS, and JavaScript for an interactive and user-friendly interface.
Data Sources: APIs for fetching real-time stock data and AI models to provide intelligent responses.
Persistence: A watchlist feature to save user-selected stocks using local storage or database integration.
AI Integration: Leveraging OpenAI to deliver contextualized insights.

## Challenges we ran into
1. Integrating multiple APIs and ensuring data consistency.
2. Designing a smooth user interface that balances simplicity and functionality.
3. Fine-tuning the AI assistant to handle complex and nuanced financial queries.
4. Connecting frontend with backend
5. Using Git and GitHub in an effective 

## Accomplishments that we're proud of

Successfully merging stock tracking and AI assistance into one cohesive platform.
Creating an intuitive interface that caters to both beginners and seasoned investors.
Implementing a feature-rich backend that delivers accurate, real-time stock data.
Fine-tuning the AI to offer meaningful, context-aware financial advice.

## What we learned

This is the first fully functional website each of our team members have built!
The power of blending data with conversational AI to create a user-centric experience.
How to tackle challenges with API integration and dynamic data handling.
The importance of user feedback in refining features and improving usability.
Best practices for building scalable and modular financial tools.

## What's next for Coinvo
Next on our roadmap:
1. Increasing functionality by adding more than our form, chatbot, and stocktracker
2. Extending our user ability to access personal data


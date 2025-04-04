import json
import openai
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
import os
import requests
import webbrowser

API_KEY_FILE = "user_api_key.txt"

# Load stored API key if available
def get_stored_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as file:
            return file.read().strip()
    return None

def save_api_key(api_key):
    with open(API_KEY_FILE, "w") as file:
        file.write(api_key)

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password", value=get_stored_api_key())

if st.sidebar.button("Save API Key"):
    save_api_key(api_key)
    st.success("API Key saved successfully!")

if not api_key:
    st.warning("Please enter your OpenAI API key to use the chatbot.")
    st.stop()
else:
    openai.api_key = api_key  # Assign user-provided key

USER_DATA_URL = "http://127.0.0.1:8000/get_user_data"
USER_DATA_FILE = "user_data.json"



def get_user_data():
    try:
        response = requests.get(USER_DATA_URL)
        if response.status_code == 200:
            return response.json()
        return {}
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to user data service.")
        return {}

#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="127.0.0.1", port=8501, reload=True)


# Function to retrieve stored user financial data
#def get_user_data():
#    response = requests.get(USER_DATA_URL)
#    if response.status_code == 200:
#       return response.json()
#    return {}

st.title("🤖 Coinvo AI:")
st.write("💡 Ask about stock trends, investment strategies, and financial insights!")

st.markdown("---")  # Adds a horizontal line

# Load user data for personalization
user_data = get_user_data()

#wow test

#openai.api_key = open('API_KEY', 'r').read()
    

def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period ='1y').iloc[-1].Close)

def calculate_SMA(ticker, window):
    data = yf.Ticker(ticker).history(period = '1y').Close
    return str(data.rolling(window=window).mean().iloc[-1])

def calculate_EMA(ticker, window):
    data = yf.Ticker(ticker).history(period = '1y').Close
    return str(data.ewm(span=window, adjust = False).mean().iloc[-1])

def calculate_RSI(ticker):
    data = yf.Ticker(ticker).history(period = '1y').Close
    delta = data.diff()
    up = delta.clip(lower = 0)
    down = -1*delta.clip(upper=0)
    ema_up = up.ewm(com=14-1, adjust = False).mean()
    ema_down = down.ewm(com=14-1, adjust = False).mean()
    rs = ema_up / ema_down
    return str(100-(100/ (1+rs)).iloc[-1])

def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period = '1y').Close
    short_EMA = data.ewm(span = 12, adjust = False).mean()
    long_EMA = data.ewm(span = 26, adjust = False).mean()
    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9, adjust = False).mean()
    MACD_histogram = MACD - signal 

    return f'{MACD[-1]}, {signal[-1]}, {MACD_histogram[-1]}'

def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period = '1y')
    plt.figure(figsize = (10, 5))
    plt.plot(data.index, data.Close)
    plt.title(f'{ticker} Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.grid(True)
    plt.savefig('stock.png')
    plt.close()


functions = [ #gpt looks here
    {
        'name': 'get_stock_price', 
        'description': 'Gets the latest stock price given the ticker symbol of a company.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example AAPL for Apple)'
                }
            },
            'required': ['ticker'],
        },
    },
    {
        'name': 'calculate_SMA', 
        'description': 'Calculate the simple moving average for a given stock ticker and a window.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example AAPL for Apple)'
                },
                'window': {
                    'type': 'integer',
                    'description': 'The timeframe to consider when calculating the SMA'
                }
            },
            'required': ['ticker', 'window'],
        },
    },
    {
        'name': 'calculate_EMA', 
        'description': 'Calculate the exponential moving average for a given stock ticker and a window.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example AAPL for Apple)'
                },
                'window': {
                    'type': 'integer',
                    'description': 'The timeframe to consider when calculating the EMA'
                }
            },
            'required': ['ticker', 'window'],
        },
    },
    {
        'name': 'calculate_RSI', 
        'description': 'Calculate the RSI for a given stock ticker.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example AAPL for Apple)'
                },
            },
            'required': ['ticker'],
        },
    },
    {
        'name': 'calculate_MACD', 
        'description': 'Calculate the MACD for a given stock ticker.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example AAPL for Apple)'
                },
            },
            'required': ['ticker'],
        },
    },
    {
        'name': 'plot_stock_price', 
        'description': 'Plot the stock price for the last year given the ticker symbol of a company.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example AAPL for Apple)'
                },
            },
            'required': ['ticker'],
        },
    },

]

available_functions = {
    'get_stock_price': get_stock_price,
    'calculate_SMA': calculate_SMA,
    'calculate_EMA': calculate_EMA,
    'calculate_RSI': calculate_RSI,
    'calculate_MACD': calculate_MACD,
    'plot_stock_price': plot_stock_price
}

#streamli
#streamlit implementation will change

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

user_input = st.text_input('Your input:')

if user_input:
    try:
        # Create a personalized AI prompt using stored user financial data
        personalized_prompt = f"""
        You are a financial advisor providing investment strategies.
        Here is the user's profile:
        - Name: {user_data.get('name', 'Unknown')}
        - Monthly Income: ${user_data.get('monthly_income', 'Unknown')}
        - Debt: ${user_data.get('debt', 'Unknown')}
        - Risk Tolerance: {user_data.get('risk_tolerance', 'Unknown')}
        
        Now answer the user's question: {user_input}
        """
        
        st.session_state['messages'].append({'role': 'user', 'content': f'{user_input}'})
        
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            #messages = st.session_state['messages'],
            messages=st.session_state['messages'] + [{"role": "system", "content": personalized_prompt}],
            functions = functions,
            function_call = 'auto'
        )
        response_message = response['choices'][0]['message']
        if response_message.get('function_call'):
            function_name = response_message['function_call']['name']
            function_args = json.loads(response_message['function_call']['arguments'])
            if function_name in ['get_stock_price', 'calculate_RSI', 'calculate_MACD', 'plot_stock_price']:
                args_dict = {'ticker': function_args.get('ticker')}
            elif function_name in ['calculate_SMA', 'calculate_EMA']:
                args_dict = {'ticker': function_args.get('ticker'), 'window': function_args.get('window')}
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**args_dict)

            if function_name == 'plot_stock_price':
                st.image('stock.png')
            else:
                st.session_state['messages'].append(response_message)
                st.session_state['messages'].append(
                    {
                        'role': 'function',
                        'name': function_name,
                        'content': function_response
                    }
                )

                second_response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages = st.session_state['messages']
                )
                st.text(second_response['choices'][0]['message']['content'])
                st.session_state['messages'].append({'role': 'assistant', 'content': second_response['choices'][0]['message']['content']})
        else:
            st.text(response_message['content'])
            st.session_state['messages'].append({'role': 'assistant', 'content': response_message['content'] })
    except Exception as e:
        raise e

# Back to Main Page Button (Opens in the same tab)
st.markdown(f"""
    <style>
        .custom-button {{
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            background-color: #007bff;
            color: white;
            font-size: 18px;
            padding: 12px 24px;
            margin-top: 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }}

        .custom-button:hover {{
            background-color: #45a049;
            transform: scale(1.05);
        }}

        .button-container {{
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }}
    </style>

    <div class="button-container">
        <a href="http://127.0.0.1:5500/tamuhack_25_jan_2/template/index.html" target="_self">
            <button class="custom-button">🏡 Back to Main Page</button>
        </a>
    </div>
""", unsafe_allow_html=True)

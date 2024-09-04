import streamlit as st
from together import Together
import requests
import os

# Define a function to fetch stock news
def fetch_stock_news(ticker, api_key, limit=10):
    url = f"https://api.polygon.io/v2/reference/news?ticker={ticker}&limit={limit}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch news, status code: {response.status_code}")
        return None

# App interface
st.title("Stock Analyzer")

ticker = st.text_input("Enter Stock Ticker:")
api_key = os.getenv("POLYGON_API_KEY")
together_client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
if st.button("Analyze Stock"):
    if ticker and api_key:
        news_data = fetch_stock_news(ticker, api_key)

        if news_data:
            summary = ""
            for article in news_data['results']:
                summary += article['description'] + "\n\n"

            # Call Together API for analysis (replace with actual Together client code)
            response = together_client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a finance expert who can analyze and provide conclusions about stocks."
                    },
                    {
                        "role": "user",
                        "content": f"""Go over the summary about the {ticker} stock given below, and give your analysis on why
                        is it a good or a bad stock right now.
                        
                        {summary}
                        
                        It should be an easy read and assertive"""
                    }
                ],
                temperature=0.11,
                top_p=1,
                top_k=50,
                repetition_penalty=1,
                stop=["<|eot_id|>"],
                max_tokens = 500
            )
            
            analysis = response.choices[0].message.content

            # Display analysis in a scrollable text box
            st.subheader("Stock Analysis")
            st.markdown(analysis)

    else:
        st.warning("Please enter both a stock ticker and API key.")
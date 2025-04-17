import streamlit as st
import requests
from bs4 import BeautifulSoup
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
# Initialize the Groq client
API_KEY = os.getev("API_KEY")#  # Replace with your Groq API Key
client = Groq(api_key=API_KEY)

# Function: Web scraping
def scrape_web(query, num_results=5):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num_results}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract search result titles and links
    results = []
    for result in soup.select(".tF2Cxc"):
        title = result.select_one(".DKV0Md").text
        link = result.select_one(".yuRUbf a")["href"]
        snippet = result.select_one(".VwiC3b").text
        results.append({"title": title, "link": link, "snippet": snippet})

    return results

# Function: Process scraped data with Groq
def process_with_groq(scraped_data, user_query):
    prompt = f"""
    Using the following web content, answer the user's query: "{user_query}"

    Web content:
    {scraped_data}

    Provide a concise, accurate, and helpful response.
    """
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=512,
    )
    return completion.choices[0].message.content.strip()

# Streamlit Application
def web_scraper_app():
    st.set_page_config(
        page_title="Web Search & AI Chatbot Assistant",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for styling
    st.markdown("""
        <style>
        .main-title {font-size: 40px; font-weight: bold; color: #4CAF50; text-align: center;}
        .sub-header {font-size: 18px; color: #555; text-align: center;}
        .section {background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin-bottom: 20px;}
        .scraped-content {border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;}
        .response-box {background-color: #e8f5e9;color: blue; border-radius: 10px; padding: 15px; margin-top: 20px;}
        </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.markdown("<div class='main-title'>Web Search & AI Chatbot Assistant 🌐🤖</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Search the web and get AI-powered answers!</div>", unsafe_allow_html=True)

    # User input section
    with st.container():
        query = st.text_input("Enter your search query:", placeholder="e.g., Benefits of machine learning")
        num_results = st.slider("Number of web pages to scrape:", 1, 10, 5)
    
    if st.button("Search and Generate Answer"):
        if query.strip():
            with st.spinner("Searching the web and generating an answer..."):
                try:
                    # Step 1: Web scraping
                    results = scrape_web(query, num_results)
                    if not results:
                        st.error("No results found. Try a different query.")
                        return

                    # Display scraped results
                    st.subheader("🔎 Scraped Web Content")
                    for i, result in enumerate(results, 1):
                        st.markdown(f"<div class='scraped-content'>", unsafe_allow_html=True)
                        st.markdown(f"**{i}. {result['title']}**")
                        st.write(f"{result['snippet']}")
                        st.write(f"[Read more]({result['link']})")
                        st.markdown("</div>", unsafe_allow_html=True)

                    # Step 2: Process with Groq
                    combined_content = "\n".join([f"{res['title']}: {res['snippet']}" for res in results])
                    answer = process_with_groq(combined_content, query)

                    # Display chatbot response
                    st.subheader("🤖 AI-Generated Answer")
                    st.markdown(f"<div class='response-box'>{answer}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a search query.")

if __name__ == "__main__":
    web_scraper_app()
import streamlit as st
from mcq_gen import mcq_app
from mem_tracker import memory_storer_app
from scrapper_generator import scrape_web

def main():
    st.set_page_config(page_title="ERGO Learning Platform", layout="wide")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose the app mode",
        ["MCQ Generator", "Memory Tracker", "Web Scraper"]
    )
    
    # Display the selected app
    if app_mode == "MCQ Generator":
        mcq_app()
    elif app_mode == "Memory Tracker":
        memory_storer_app()
    elif app_mode == "Web Scraper":
        scrape_web()

if __name__ == "__main__":
    main() 
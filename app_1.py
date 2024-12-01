import streamlit as st
from mcq_gen import mcq_app
from scrapper_generator import web_scraper_app
from mem_tracker import memory_storer_app
# from app import main as rag_app

st.set_page_config(
    page_title="AI Educational Assistant",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)
def main():
    st.title("AI Educational Assistant 📚🤖")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    app_choice = st.sidebar.radio(
        "Choose a Feature:",
        ["MCQ Generator", "Web Scraper & AI Generator", "Memory Storer & Summarizer", "RAG Application"]
    )

    # Load selected page
    if app_choice == "MCQ Generator":
        mcq_app()
    elif app_choice == "Web Scraper & AI Generator":
        web_scraper_app()
    elif app_choice == "Memory Storer & Summarizer":
        memory_storer_app()
    elif app_choice == "RAG Application":
        # rag_app()
        pass

if __name__ == "__main__":
    main()

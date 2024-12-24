import streamlit as st
import sqlite3
from datetime import datetime
from groq import Groq

# Initialize the Groq client
API_KEY = "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"  # Replace with your actual API Key
client = Groq(api_key=API_KEY)

# Database setup
def init_db():
    conn = sqlite3.connect("learning_memory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT, 
            query TEXT,
            response TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

# Add entry to the database
def add_to_memory(query, response, content):
    conn = sqlite3.connect("learning_memory.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO memory (timestamp, query, response, content)
        VALUES (?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), query, response, content))
    conn.commit()
    conn.close()

# Retrieve all memory
def get_memory():
    conn = sqlite3.connect("learning_memory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memory")
    data = cursor.fetchall()
    conn.close()
    return data

# Generative AI: Summarize learning progress
def summarize_learning(memory_data):
    combined_content = "\n".join([f"Query: {row[2]}, Response: {row[3]}, Content: {row[4]}" for row in memory_data])
    prompt = f"""
    Summarize the user's learning journey based on the following interactions:
    {combined_content}
    """
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert at summarizing learning journeys."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=512,
    )
    return completion.choices[0].message.content.strip()

# Streamlit Application with Enhanced GUI
def memory_storer_app():
    st.set_page_config(
        page_title="Memory-Based Learning Tracker",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar
    st.sidebar.title("📚 Learning Tracker")
    st.sidebar.markdown("Easily track and summarize your learning journey.")
    menu = st.sidebar.radio("Navigate", ["Learn", "Memory", "Summarize"])

    # Apply Custom Styling
    st.markdown("""
        <style>
        .main-title {font-size: 50px; font-weight: bold; text-align: center; color: #4CAF50;}
        .sub-title {font-size: 24px; color: #555;}
        .section {background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 15px;}
        .memory-box {border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;}
        .memory-timestamp {font-size: 12px; color: #888;}
        .memory-content {font-size: 16px; color: #333;}
        </style>
    """, unsafe_allow_html=True)

    # Initialize database
    init_db()

    if menu == "Learn":
        st.markdown("<div class='main-title'>Learn Something New 🧠</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Ask a question to explore and expand your knowledge.</div>", unsafe_allow_html=True)
        
        # User input for learning
        query = st.text_input("Enter your query:", placeholder="e.g., Explain Newton's laws of motion")
        if st.button("Learn"):
            if query.strip():
                with st.spinner("Fetching response..."):
                    try:
                        # Simulate a response
                        prompt = f"Provide a detailed explanation for: {query}"
                        completion = client.chat.completions.create(
                            model="llama3-8b-8192",
                            messages=[
                                {"role": "system", "content": "You are a helpful teacher."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=512,
                        )
                        response = completion.choices[0].message.content.strip()

                        # Store in memory
                        add_to_memory(query, response, "General Knowledge")

                        # Display response
                        st.subheader("AI Response")
                        st.markdown(f"<div class='section'>{response}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter a valid query.")

    elif menu == "Memory":
        st.markdown("<div class='main-title'>Your Learning Memory 📖</div>", unsafe_allow_html=True)
        memory_data = get_memory()
        if memory_data:
            for row in memory_data:
                st.markdown(f"""
                    <div class='memory-box'>
                        <div class='memory-timestamp'>Timestamp: {row[1]}</div>
                        <div class='memory-content'><strong>Query:</strong> {row[2]}</div>
                        <div class='memory-content'><strong>Response:</strong> {row[3]}</div>
                        <div class='memory-content'><strong>Content:</strong> {row[4]}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No learning data available yet.")

    elif menu == "Summarize":
        st.markdown("<div class='main-title'>Summarize My Learning Journey 📊</div>", unsafe_allow_html=True)
        memory_data = get_memory()
        if memory_data:
            if st.button("Generate Summary"):
                with st.spinner("Generating summary..."):
                    try:
                        summary = summarize_learning(memory_data)
                        st.subheader("Learning Journey Summary")
                        st.markdown(f"<div class='section'>{summary}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
        else:
            st.info("You need to learn something first before generating a summary.")

if __name__ == "__main__":
    memory_storer_app()

import streamlit as st
import json
from groq import Groq

# Initialize the Groq client
API_KEY = "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"  # Replace with your actual API key
client = Groq(api_key=API_KEY)

# Function to extract and parse JSON from the Groq response
def extract_json_from_response(response_content):
    try:
        # Locate the JSON block in the response
        json_start = response_content.find("[")
        json_end = response_content.rfind("]") + 1
        if json_start == -1 or json_end == -1:
            raise ValueError("JSON block not found in the response.")

        # Extract and parse JSON
        json_data = response_content[json_start:json_end]
        mcqs = json.loads(json_data)
        return mcqs
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON: {e}\nExtracted data: {response_content[json_start:json_end]}")

# Function to generate MCQs using the Groq API
def generate_mcqs_with_groq(topic, num_questions=5):
    prompt = f"""
    Generate {num_questions} multiple-choice questions on the topic "{topic}". 
    Each question should include:
    - A question string.
    - Four options in a list.
    - A string indicating the correct answer.

    Provide the output in valid JSON format as:
    [
        {{
            "question": "Sample question?",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correct_option": "Option 1"
        }},
        ...
    ]
    """
    try:
        # Interact with Groq API
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are an expert at creating MCQs."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        # Extract response content
        response_content = completion.choices[0].message.content.strip()
        
        if not response_content:
            raise ValueError("API returned an empty response.")

        # Extract and parse JSON
        return extract_json_from_response(response_content)

    except Exception as e:
        raise ValueError(f"Unexpected error: {e}")

# Streamlit App
def mcq_app():
    st.title("Test BOT - ⚡️")
    st.write("Generate multiple-choice questions (MCQs) on any topic of your choice!")
    
    # User inputs
    topic = st.text_input("Enter a topic:", placeholder="e.g., Physics, Chemistry, Motor Parts")
    num_questions = st.slider("Number of questions:", min_value=1, max_value=10, value=5)
    
    if st.button("Generate MCQs"):
        if topic.strip():
            with st.spinner("Generating MCQs..."):
                try:
                    mcqs = generate_mcqs_with_groq(topic, num_questions)
                    st.session_state['mcqs'] = mcqs
                    st.session_state['answers'] = {}  # Reset answers
                    st.success(f"Generated {len(mcqs)} MCQs on '{topic}'. Scroll down to solve them!")
                except Exception as e:
                    st.error(f"Error generating MCQs: {str(e)}")
        else:
            st.warning("Please enter a valid topic.")

    if 'mcqs' in st.session_state:
        st.markdown("## Solve the MCQs")
        for i, mcq in enumerate(st.session_state['mcqs'], 1):
            question_key = f"q{i}"
            st.markdown(f"**Q{i}:** {mcq['question']}")
            st.radio(
    f"Select your answer for Q{i}:",
    options=mcq['options'],
                key=question_key,
            )   
            st.markdown("---")

        if st.button("Submit Answers"):
            st.session_state['answers'] = {
                f"q{i}": st.session_state.get(f"q{i}")
                for i in range(1, len(st.session_state['mcqs']) + 1)
            }
            st.session_state['show_answers'] = True

    if st.session_state.get('show_answers'):
        st.markdown("## Correct Answers and Feedback")
        correct_count = 0
        for i, mcq in enumerate(st.session_state['mcqs'], 1):
            user_answer = st.session_state['answers'].get(f"q{i}")
            correct_answer = mcq['correct_option']
            st.markdown(f"**Q{i}:** {mcq['question']}")
            st.write(f"**Your Answer:** {user_answer}")
            st.write(f"**Correct Answer:** {correct_answer}")
            if user_answer == correct_answer:
                st.success("✅ Correct!")
                correct_count += 1
            else:
                st.error("❌ Incorrect.")
            st.markdown("---")
        st.write(f"**You got {correct_count}/{len(st.session_state['mcqs'])} correct!**")

# Run the app
if __name__ == "__main__":
    main()

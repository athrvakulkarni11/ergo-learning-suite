import json
from groq import Groq

API_KEY = "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"
client = Groq(api_key=API_KEY)

def test_groq_api():
    prompt = "Generate 2 multiple-choice questions about Physics in JSON format."
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": "You are an expert at generating questions."},
                  {"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7
    )
    print("Response:", completion.choices[0].message.content)

test_groq_api()

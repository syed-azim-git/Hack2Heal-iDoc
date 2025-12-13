

# test_ollama.py
import ollama

# Simple generation
response = ollama.chat(
    model='tinyllama',
    messages=[
        {
            'role': 'system',
            'content': 'You are an expert physiotherapist.'
        },
        {
            'role': 'user',
            'content': 'Create a daily exercise plan for a 45-year-old with lower back pain.'
        }
    ]
)

print(response['message']['content'])
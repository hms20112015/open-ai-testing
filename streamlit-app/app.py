import streamlit as st
from openai import OpenAI
import time
from functools import wraps

# Initialize OpenAI client
client = OpenAI()

# Define the maximum API call rate (calls per second)
MAX_CALL_RATE = .01  # Adjust this value as needed

def throttle_api_calls(func):
    """
    Decorator function to throttle API calls.
    """
    last_call_time = 15
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal last_call_time
        current_time = time.time()
        elapsed_time = current_time - last_call_time
        if elapsed_time < 1 / MAX_CALL_RATE:
            time.sleep(1 / MAX_CALL_RATE - elapsed_time)
        last_call_time = time.time()
        return func(*args, **kwargs)
    
    return wrapper

@throttle_api_calls
def generate_response(user_input):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair. You value brevity and clarity. You also use correct grammar and proper spacing and punctuation."},
            {"role": "user", "content": user_input}
        ]
    )
    # Extracting the generated poem from the completion message object
    poem_parts = completion.choices[0].message.content
    # If the poem is represented as a list, join the parts into a single string
    if isinstance(poem_parts, list):
        poem = ''.join(poem_parts)
    else:
        poem = poem_parts
    # Replace newline characters with an empty string
    cleaned_poem = poem.replace('\n', '')
    return cleaned_poem

def main():
    st.title('Perry the Poetic Programming Tutor')

    user_input = st.text_input("Ask me a question about programming:")

    if st.button('Generate Poem'):
        response = generate_response(user_input)
        # Displaying the generated poem
        st.subheader("Topic Explanation:")
        st.write(response)

if __name__ == '__main__':
    main()

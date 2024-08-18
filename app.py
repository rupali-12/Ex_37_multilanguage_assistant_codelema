import requests
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and model ID from environment variables
api_key = os.getenv("GROQ_API_KEY")
model_id = os.getenv("MODEL_ID")

# Function to send prompt to the API and get a response
def get_api_response(prompt):
    api_url = "https://api.groq.com/openai/v1/chat/completions"  # Replace with the actual API URL
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raises HTTPError for bad responses

        if response.status_code == 200:
            response_data = response.json()
            # Extract necessary information from response_data
            return response_data.get('choices', [{}])[0].get('message', {}).get('content', 'No result found.')
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Exception occurred: {str(e)}"

# Streamlit interface
st.set_page_config(page_title="Multilanguage Code Assistant", page_icon=":robot_face:")

# Custom CSS for styling
st.markdown("""
    <style>
        .main-container {
            background-color: #f7f7f9;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            max-width: 800px;
            margin: 0 auto;
        }
        .header {
            font-size: 2.5rem;
            color: #333;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .instructions {
            font-size: 1.2rem;
            color: #555;
            text-align: center;
            margin-bottom: 2rem;
        }
        .text-input {
            margin-bottom: 1.5rem;
        }
        .response-area {
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #fff;
            padding: 1rem;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }
        .footer {
            text-align: center;
            margin-top: 2rem;
            color: #777;
        }
    </style>
""", unsafe_allow_html=True)

# Main layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Main title
st.markdown('<div class="header">Multilanguage Code Assistant</div>', unsafe_allow_html=True)

# Instructions
st.markdown('<div class="instructions">Enter your query below to generate a code snippet in the desired language. Click the button to get the response.</div>', unsafe_allow_html=True)

# User input
prompt = st.text_input("Enter your query:", key="query", placeholder="Type your query here...", label_visibility="hidden")

# Button and response area
if st.button("Generate Code"):
    if prompt:
        with st.spinner("Generating code..."):
            response = get_api_response(prompt)
            if "Error" in response or "Exception" in response:
                st.error(response)
            else:
                st.success("Code generated successfully!")
                st.markdown('<div class="response-area">', unsafe_allow_html=True)
                st.text_area("Generated Code:", value=response, height=200, key="response")
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a query.")

st.markdown('<div class="footer">Powered by Multilanguage Code Assistant</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

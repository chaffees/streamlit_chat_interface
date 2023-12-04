import streamlit as st
from io import StringIO
import boto3
import json

# AWS configuration
aws_region = 'us-east-1'
sagemaker_runtime = boto3.client('sagemaker-runtime', region_name=aws_region)
sagemaker_endpoint_name = 'your_sagemaker_endpoint'

# Initialize session state variables
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []
if 'max_tokens' not in st.session_state:
    st.session_state['max_tokens'] = 200
if 'temperature' not in st.session_state:
    st.session_state['temperature'] = 0.7
if 'seed' not in st.session_state:
    st.session_state['seed'] = 0

def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        return StringIO(uploaded_file.getvalue().decode("utf-8")).read()
    return None

def format_input(user_input):
    return user_input.strip()

def get_model_response(message):
    formatted_message = {
        "inputs": format_input(message),
        "parameters": {
            "max_tokens": st.session_state['max_tokens'],
            "temperature": st.session_state['temperature'],
            "seed": st.session_state['seed']
        }
    }
    json_message = json.dumps(formatted_message)
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=sagemaker_endpoint_name,
        ContentType='application/json',
        Body=json_message
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        response_body = response['Body'].read().decode('utf-8')
        response_json = json.loads(response_body)
        if isinstance(response_json, list) and len(response_json) > 0:
            full_response = response_json[0].get('generated_text', '')
            return full_response.split(message)[-1].strip()
        else:
            return "Unexpected response format"
    else:
        st.error('Model request failed with status code: ' +
                 str(response['ResponseMetadata']['HTTPStatusCode']))
        return None

# Streamlit UI Setup
st.title('Multifunctional Chatbot with Amazon SageMaker')

with st.sidebar:
    st.title("Conversation Setup")
    clear_conversation_button = st.button("Clear Conversation")
    uploaded_file = st.file_uploader("Upload a file", type=['txt', 'png', 'jpg', 'jpeg', 'mp3', 'wav'])
    st.session_state['max_tokens'] = st.slider("Number of tokens to generate", 8, 1024, st.session_state['max_tokens'])
    st.session_state['temperature'] = st.slider("Temperature", 0.0, 2.5, st.session_state['temperature'])
    st.session_state['seed'] = st.slider("Random seed", 0, 1000, st.session_state['seed'])

user_input = st.text_area("Input text:", height=100)
send_button = st.button("Send")
response_container = st.container()

if send_button and user_input:
    processed_text = process_uploaded_file(uploaded_file) if uploaded_file else user_input
    response = get_model_response(processed_text)
    st.session_state['conversation'].append(f"User: {processed_text}")
    st.session_state['conversation'].append(f"AI: {response}")
    with response_container:
        for line in st.session_state['conversation']:
            st.write(line)

if clear_conversation_button:
    st.session_state['conversation'] = []


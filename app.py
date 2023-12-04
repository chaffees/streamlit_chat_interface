import streamlit as st
from io import StringIO
import boto3
import json

# AWS configuration
aws_region = 'us-east-1'
sagemaker_runtime = boto3.client('sagemaker-runtime', region_name=aws_region)
sagemaker_endpoint_name = 'your_sagemaker_endpoint'

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        return text
    return None

def format_input(user_input):
    # Format input with special tags as per model requirement
    formatted_input = f"INST: CHAT <<SYS>> {user_input.strip()} <<EOS>>"
    return formatted_input

def get_model_response(message):
    formatted_message = {"inputs": format_input(message)}
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
            full_response = response_json[0].get('generated_text', 'No response')
            # Extracting only the response part after the input
            answer = full_response.split('<<EOS>>')[-1].strip()
            return answer
        else:
            return "Unexpected response format"
    else:
        st.error('Model request failed with status code: ' +
                 str(response['ResponseMetadata']['HTTPStatusCode']))
        return None

# Streamlit UI
st.title('Multifunctional Chatbot with Llama-2-70b-hf')

with st.sidebar:
    st.title("Conversation Setup")
    clear_conversation_button = st.button("Clear Conversation")
    uploaded_file = st.file_uploader("Upload a file", type=['txt', 'png', 'jpg', 'jpeg', 'mp3', 'wav'])

user_input = st.text_area("Input text:", height=100)
send_button = st.button("Send")
response_container = st.container()

if send_button and user_input:
    processed_text = process_uploaded_file(uploaded_file) if uploaded_file else user_input
    response = get_model_response(processed_text)
    st.session_state['past'].append(processed_text)
    st.session_state['generated'].append(response)
    with response_container:
        for past_input, gen_response in zip(st.session_state['past'], st.session_state['generated']):
            st.write(f"User: {past_input}")
            st.write(f"AI: {gen_response}")

if clear_conversation_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    user_input = ""

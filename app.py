import streamlit as st
from io import StringIO
from content_handler_module import ContentHandler
from langchain.llms import SagemakerEndpoint
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from random import randint
import boto3

# AWS configuration
aws_region = 'us-east-1'  # Set your AWS region
sagemaker_client = boto3.client('sagemaker')
sagemaker_endpoint_name = 'your_sagemaker_endpoint_name'  # Set your SageMaker endpoint name

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'max_tokens' not in st.session_state:
    st.session_state['max_tokens'] = 200
if 'temperature' not in st.session_state:
    st.session_state['temperature'] = 0.7
if 'seed' not in st.session_state:
    st.session_state['seed'] = 0

# Function to process uploaded files
def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        return text
    return None

# Title of your application
st.title('Building a multifunctional chatbot with Amazon SageMaker')

# Sidebar for setup options
with st.sidebar:
    st.title("Conversation setup")
    clear_conversation_button = st.button("Clear Conversation")
    uploaded_file = st.file_uploader("Upload a file", type=['txt', 'png', 'jpg', 'jpeg', 'mp3', 'wav'])
    use_knowledge_base = st.checkbox('Use knowledge base')
    st.session_state['max_tokens'] = st.slider("Number of tokens to generate", 8, 1024, st.session_state['max_tokens'])
    st.session_state['temperature'] = st.slider("Temperature", 0.0, 2.5, st.session_state['temperature'])
    st.session_state['seed'] = st.slider("Random seed", 0, 1000, st.session_state['seed'])

# Main conversational interface
user_input = st.text_area("Input text:", height=100)
send_button = st.button("Send")
response_container = st.container()

# Create Conversation Chain with Memory
@st.cache_resource
def load_chain(endpoint_name, aws_region):
    memory = ConversationBufferMemory(return_messages=True)
    llm = SagemakerEndpoint(
        endpoint_name=endpoint_name,
        region_name=aws_region,
        content_handler=ContentHandler()
    )
    chain = ConversationChain(llm=llm, memory=memory)
    return chain

chatchain = load_chain(sagemaker_endpoint_name, aws_region)

# Logic for send button
if send_button and user_input:
    processed_text = process_uploaded_file(uploaded_file) if uploaded_file else user_input
    response = chatchain(processed_text)["response"]
    st.session_state['past'].append(processed_text)
    st.session_state['generated'].append(response)
    with response_container:
        for past_input, gen_response in zip(st.session_state['past'], st.session_state['generated']):
            st.write(f"User: {past_input}")
            st.write(f"AI: {gen_response}")

# Logic for clear button in sidebar
if clear_conversation_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    user_input = ""

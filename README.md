# Streamlit Chat Interface

## Description
This project is a Streamlit-based web application designed to provide a multifunctional chat interface. It integrates with Amazon SageMaker, allowing users to interact with machine learning models for various purposes, such as generating responses or processing information.

## Features
- Interactive chat interface built with Streamlit.
- Integration with Amazon SageMaker for advanced machine learning capabilities.
- Customizable conversation settings including token generation and temperature control.

## Prerequisites
- Python 3.x
- Streamlit
- Boto3 (AWS SDK for Python)
- AWS account with SageMaker access

## Setup and Installation
1. **Clone the Repository:**
   `git clone https://github.com/chaffees/streamlit_chat_interface.git`
   `cd streamlit_chat_interface`
2. **Install Dependencies:**
   `pip install streamlit boto3`
3. **Configure AWS Credentials:**
   Set up your AWS credentials to allow the application to interact with SageMaker.
4. **Run the Streamlit Application:**
   `streamlit run app.py`

## Usage
- Start the Streamlit application and navigate to the provided local URL.
- Use the chat interface to send messages.
- Adjust conversation settings in the sidebar, such as the number of tokens, temperature, and random seed.
- Optionally, upload files for processing in the chat interface.

## Additional Information
- **SageMaker Integration:** The application communicates with a SageMaker endpoint to process user inputs. See `app.py` for implementation details.
- **Content Handler Module:** Custom content handling logic for SageMaker responses is detailed in a specific module (specify the module name).

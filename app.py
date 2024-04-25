import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

def generate_response(model, prompt, temperature, max_tokens):
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        stream=False
    )
    return completion.choices[0].message.content

# Streamlit user interface
st.set_page_config(page_title="DataSarva", layout="wide")

# Custom CSS styling
st.markdown(
    """
    <style>
        .stTextArea label, .stSlider label {
            font-size: 18px;
            font-weight: bold;
        }
        .stTextArea textarea, .stSlider .widget {
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        .stButton button {
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 8px;
            background-color: #007bff;
            color: #fff;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #0056b3;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
col1, col2, col3 = st.columns([2, 2, 1])
with col3:
    # st.image("DataSarva.png", width=100)
    st.title("DataSarva")
    st.write("Developed by Akhil Gurrapu")

# Divide the page into columns
col4, col5 = st.columns([2, 3])

with col4:
    st.subheader('Chat with below LLM models')
    # List of available models
    model_names = ["Snowflake-Arctic", "Meta-Llama3-70B", "Meta-Llama3-8B", "Mistral-8x22B", "Google-CodeGemma-7B", "Google-Gemma-7B"]
    model_values = ["snowflake/arctic", "meta/llama3-70b-instruct", "meta/llama3-8b-instruct", "mistralai/mixtral-8x22b-instruct-v0.1", "google/codegemma-7b", "google/gemma-7b"]
    # Filter buttons for model selection
    selected_model_value = st.radio("Select a model", model_values, index=1, format_func=lambda x: model_names[model_values.index(x)])

with col5:
    with st.form(key='query_form'):
        st.write(f"Selected Model: {model_names[model_values.index(selected_model_value)]}")
        prompt = st.text_area("Enter your prompt:", height=300)
        col6, col7 = st.columns(2)
        with col6:
            temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.01, label_visibility="visible")
        with col7:
            max_tokens = st.slider("Max Tokens", 100, 1500, 1024, step=10, label_visibility="visible")
        submit_button = st.form_submit_button(label='Submit', use_container_width=True)

        if submit_button and prompt:
            with st.spinner("Generating response..."):
                response = generate_response(selected_model_value, prompt, temperature, max_tokens)
            st.success(response)
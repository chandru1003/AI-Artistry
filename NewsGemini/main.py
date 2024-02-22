import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv() # loading all the envrionmant variable
import google.generativeai as genai


genai.configure(api_key="Google_api_key")


def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text
## Streamlit App

st.set_page_config(page_title="NewsGemini")
st.header("NewsGemini")

input_text = st.text_area("Artical: ", key="input")
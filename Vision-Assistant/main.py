import os
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
load_dotenv() # loading all the envrionmant variable
import google.generativeai as genai

genai.configure(api_key=os.getenv("Google_api_key"))

def get_gemini_repsonse(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_step(uploaded_file):
    if uploaded_file is not None:
        byte_data=uploaded_file.getvalue()
        
        imgParts=[
            {
                "mime_type" : uploaded_file.type,
                "data": byte_data
            }
        ]
        return imgParts
    else:
        return FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title="Vision Assistant Bot")
st.header("Vision bot")
input=st.text_input("Chat with image: ", key="input")
uploaded_file =st.file_uploader("chosse an image...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image =Image.open(uploaded_file)
    st.image(image, caption="uploaded image", use_column_width=True)
submit=st.button("Generate")    

if submit:
    image_data=input_step(uploaded_file)
    response=get_gemini_repsonse(input,image_data)
    st.subheader("The Response is")
    st.write(response)
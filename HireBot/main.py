import os
import io
import pandas as pd
import base64
import streamlit as st
import pdf2image
from dotenv import load_dotenv 
load_dotenv()
import google.generativeai as genai

genai.configure(api_key="Google_api_key")

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        poppler_path = r'F:\soft\poppler-23.11.0\Library\bin'  # Specify the Poppler binary path
        images=pdf2image.convert_from_bytes(uploaded_file.read(),poppler_path=poppler_path)
        

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def write_to_excel(response):
    print(response)
    #response_values = [value.strip() for value in response.split('|') if value.strip()]
    rows = response.split('\n')[2:]
    columns_values=response.split('\n')
    print("\n")
    print("rows are")
    print(rows)
    print("\n")
    columns = [col.strip() for col in columns_values[0].split('|') if col.strip()]
    print("columns are")
    print(columns)
    data_values = [value.strip() for value in rows[0].split('|') if value.strip()]
    # Creating a DataFrame
    df = pd.DataFrame([data_values], columns=columns)
    df.to_csv('ResumeTrackStatus.csv', index=False)
        
## Streamlit App

st.set_page_config(page_title="HireBot")
st.header("Hirebot")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file and input_text is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")


input_prompt1 = """
Act as an experienced Technical Human Resource Manager, your objective is to evaluate the provided resume against the job description. Your assessment should focus on determining whether the candidate's profile aligns with the role requirements. Please provide your professional evaluation using the following table structure:

| Name | Email | Phone | Experience | Skills | Percentage | Strengths | Weaknesses | Decision (selected or not) |
|------|-------|-------|------------|--------|------------|-----------|-------------|---------------------------|
,"""
						

if submit1:
    if uploaded_file and input_text is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
        print("response is :\n")
        write_to_excel(response)
        
    else:
        st.write("Resume or job description not found")





   





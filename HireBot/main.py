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


def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        poppler_path = r'F:\soft\poppler-23.11.0\Library\bin'  # Specify the Poppler binary path
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)
        
        first_page = images[0]

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

def write_to_excel(response, file_path):
    rows = response.split('\n')[2:]
    columns_values = response.split('\n')
    columns = [col.strip() for col in columns_values[0].split('|') if col.strip()]
    data_values = [value.strip() for value in rows[0].split('|') if value.strip()]
    
    # Add file path as a row
    file_row = ['File Path'] + [file_path] + [''] * (len(columns) - 2)  # Assuming the file path should be inserted in the second column
    
    # Creating a DataFrame
    df = pd.DataFrame([data_values], columns=columns)
    
    # Append to CSV file
    with open('ResumeTrackStatus.csv', 'a') as f:
        df.to_csv(f, header=f.tell()==0, index=False)
        
## Streamlit App

st.set_page_config(page_title="HireBot", page_icon="icon\898_815783_TopCV_BeatingtheBotsATS_Hero.ico")
st.header("Hirebot")

input_text = st.text_area("Job Description: ", key="input")
folder_path = st.text_input("Enter the folder path where resume PDF files are present: ")

if st.button("Tell Me About the Resumes"):

    if folder_path and input_text is not None:
        st.write(f"Resumes in Folder: {folder_path}")
        st.write("Generating Responses...")

        for resume_file in os.listdir(folder_path):
            if resume_file.endswith(".pdf"):
                resume_file_path = os.path.join(folder_path, resume_file)
                pdf_content = input_pdf_setup(open(resume_file_path, 'rb'))

                input_prompt1 = f"""
Act as an experienced Technical Human Resource Manager, your objective is to evaluate the provided resume against the job description. Your assessment should focus on determining whether the candidate's profile aligns with the role requirements. Please provide your professional evaluation using the following table structure:

| Name | Email | Phone | Experience | Skills | matching Percentage | Strengths | Weaknesses | Decision (selected or not) |
|------|-------|-------|------------|--------|------------|-----------|-------------|---------------------------|

note: The "matching Percentage" column represents how well the resume matches the job description. Make decisions based on the following criteria:

If the matching Percentage is greater than 80%, recommend scheduling an interview.
If the matching Percentage is between 70% and 80%, consider placing the resume on hold.
If the matching Percentage is between 60% and 70%, mark it for discussion.
If the matching Percentagee is below 60%, reject the resume.

.Evaluation for {resume_file}
                            """

                response = get_gemini_response(input_text, pdf_content, input_prompt1)

                st.subheader(f"Response for {resume_file}")
                st.write(response)
                
                write_to_excel(response, 'ResumeTrackStatus.csv')

        st.write("Responses generated and saved to 'ResumeTrackStatus.csv'.")
    else:
        st.write("Please provide the folder path and job description.")
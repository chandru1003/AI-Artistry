import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv() # loading all the envrionmant variable
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("Google_api_key"))

def generate_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)    
    return response.text

def extract_video(url):
    try:
        video_id=url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript =""
        for i in transcript_text:
            transcript +=" "+i["text"]
    except Exception as e:
        raise e
    return transcript


st.title("SummaryChat")
input_prompt=st.text_input("Chat with video: ", key="input")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Generate"):
    transcript_text=extract_video(youtube_link)

    if transcript_text:
        summary=generate_content(transcript_text,input_prompt)
        st.markdown("### Answer")
        st.write(summary)


import streamlit as st
import google.generativeai as genai


genai.configure(api_key="Your_Google_API_Key")


def generate_newspaper_article(full_article):
  
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(full_article)
    return response.text

# Streamlit app
def main():
    st.title("NewsGemini: Newspaper Article Generator")
    st.markdown("---")
    

    full_article = st.text_area("Input Full Article", height=200)

    if st.button("Generate Newspaper Article"):
        if full_article:
           
            newspaper_article = generate_newspaper_article(full_article)
            st.subheader("Generated Newspaper Article:")
            st.write(newspaper_article)
        else:
            st.warning("Please input a full article.")

if __name__ == "__main__":
    main()

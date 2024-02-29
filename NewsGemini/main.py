import streamlit as st
import google.generativeai as genai

# Configure Gemini model with API key
genai.configure(api_key="Google_api_key")

# Function to generate newspaper article
def generate_newspaper_article(raw_article):
    prompt = """
   Act as a newspaper editor, analyze the raw inputs, and generate an India newspaper-style article. Include the following elements:

Headline: The main title of the article, summarizing its content and attracting readers' attention.
Byline: The author's name or credit line indicating who wrote the article.
Lead: The introductory paragraph that provides a brief overview or summary of the article's main points.
Body: The main content of the article, consisting of multiple paragraphs elaborating on the topic.
Tail: The concluding section that may include additional information, quotes, or reflections on the topic.
    
    """ + raw_article + """
    """
    # Use Gemini model to generate newspaper article
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# Streamlit app
def main():
    st.title("NewsGemini: Newspaper Article Generator")
    st.markdown("---")

    # Input full article
    raw_article = st.text_area("Input Full Article", height=200)

    if st.button("Generate Newspaper Article"):
        if raw_article:
            # Generate newspaper article
            newspaper_article = generate_newspaper_article(raw_article)
            st.subheader("Generated Newspaper Article:")
     
            st.subheader(newspaper_article.split('\n')[0])  # Display headline
            
            st.write("\n".join(newspaper_article.split('\n')[1:]))  # Display article content
        else:
            st.warning("Please input a full article.")

if __name__ == "__main__":
    main()

# SummaryChat

This application utilizes Generative AI to generate summaries based on video transcripts and user input. Users can input a chat prompt along with a YouTube video link, and the application will generate a summary based on the video's transcript and the provided prompt.

## Setup Instructions:

1. **Environment Setup:**
   - Ensure you have Python installed on your system.
   - Use `pip` to install the required Python packages:
     ```
     pip install -r requirements.txt   
     ```

   - Add your Google API key to the `.env` file:
     ```
     Google_api_key=YOUR_API_KEY
     ```

3. **Running the Application:**
   - Open a terminal or command prompt.
   - Navigate to the project directory.
   - Run the Streamlit application:
     ```
     streamlit run main.py
     ```

## Usage Guide:

- **Chat with Video:**
  - Enter your chat prompt in this text box. This will guide the generation of the summary based on the video content.

- **Enter YouTube Video Link:**
  - Paste the link to the YouTube video you want to summarize. The application will display the thumbnail of the video for reference.

- **Generate:**
  - Click this button to initiate the generation process. The application will extract the video transcript, generate a summary based on the transcript and input prompt, and display the result.

## Acknowledgements:

- **Streamlit:** This application is built using Streamlit, an open-source Python library for building interactive web applications.

- **Google Generative AI:** The generative AI models used in this application are provided by Google's Generative AI service, enabling the creation of contextual and insightful summaries.

- **YouTube Transcript API:** This application utilizes the YouTube Transcript API to extract video transcripts, facilitating the generation of summaries.


**Note:** Ensure that you have appropriate permissions and usage rights for the videos and transcripts used with this application. This project is for educational and demonstration purposes only.

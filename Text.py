import streamlit as st
import requests
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play
import io
import time

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HUGGING_FACE_TOKEN = "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"
headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}

API_URL_IMG = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers_img = {"Authorization": "Bearer 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"}

def main():

    selected_option = st.sidebar.radio("Select option:", ["Text_summarization", "Img_to_text","Text_sentiment","Text_to_audio","Text_to_speech","Text_to_flag","Text_to_img"])
    
    if selected_option == "Text_summarization":
        summary_text()
    elif selected_option == "Img_to_text":
        img_to_text()
    elif selected_option == "Text_sentiment":
        Text_sentiment()
    elif selected_option == "Text_to_audio":
        Text_to_audio()
    elif selected_option == "Text_to_speech":
        Text_to_speech()
    elif selected_option == "Text_to_flag":
        Text_to_flag() 
    elif selected_option == "Text_to_img":
        Text_to_img()  
# Set title with larger font size using HTML h1 tag
st.markdown("<h1 style='text-align: center; font-size: 35px;'>🤖 Testing Hugging Face Models with APIs by Rao_Hammad_Raza 🚀</h1>", unsafe_allow_html=True)

# text summary code
def summary_text():
    st.header("Text Summarization")
    user_input = st.text_area("Enter your prompt:")
    
    if st.button("Generate Response"):
        payload = {"inputs": user_input}
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
            output = response.json()

            if "error" in output:
                st.error(f"Error: {output['error']}")
            else:
                summary_text = output[0].get("summary_text", "No response received")
                # Display the result in an info box
                st.info(summary_text)
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")

# img to text     
def img_to_text():
    st.header("Image to Text")
    st.write("Upload an image, and the model will generate a caption for it.")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_content = uploaded_file.read()
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        
        if st.button("Generate Caption"):
            try:
                response = requests.post(API_URL_IMG, headers=headers_img, data=image_content)
                response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
                result = response.json()
                st.text(result)
            except requests.exceptions.RequestException as e:
                st.error(f"Request error: {e}")

# text sentiments
def Text_sentiment():
    st.header("Text Sentiments")
    API_URL = "https://api-inference.huggingface.co/models/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
    headers = {"Authorization": "Bearer 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"}
    # Input text area
    user_input = st.text_area("Enter your financial news text:")
    
    if st.button("Generate Sentiment Analysis"):
        payload = {"inputs": user_input}
        retries = 3

        while retries > 0:
            try:
                response = requests.post(API_URL, headers=headers, json=payload)
                response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)

                if response.status_code == 200:
                    output = response.json()
                    
                    # Display sentiment analysis results in a more readable format
                    if isinstance(output, list) and output:
                        for idx, item in enumerate(output[0]):
                            # st.subheader(f"Result {idx + 1}:")
                            st.write(f"Label: {item['label']}")
                            st.write(f"Score: {item['score']:.4f}")
                            st.write("\n")
                    else:
                        st.warning("Invalid or empty response received.")

                    # Break out of the loop if successful
                    break

            except requests.exceptions.RequestException as e:
                st.warning(f"Request error: {e}")
                retries -= 1
                time.sleep(1)  # Add a delay before retrying

        if retries == 0:
            st.error("Failed to get a response after multiple attempts. Please try again later.")

# text to audio 
def Text_to_audio():
    st.header("Text to Audio Music")
    API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
    headers = {"Authorization": "Bearer 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"}
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content if response.status_code == 200 else None
    st.write("Generate music based on your preferences!")
    # Input text area for music preferences
    music_preferences = st.text_area("Enter your music preferences:", "liquid drum and bass, atmospheric synths, airy sounds")
    if st.button("Generate Music"):
        payload = {"inputs": music_preferences}
        audio_bytes = query(payload)

        if audio_bytes:
            # Display the generated audio
            st.audio(audio_bytes, format="audio/wav", start_time=0)
            # Add a download button for the audio
            st.download_button("Download Audio", audio_bytes, file_name="output_audio.wav", key="download_audio")

# text to speech
def Text_to_speech():
    st.header("Text to Speech")
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"
    headers = {"Authorization": "Bearer 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"}
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content
    text = st.text_area("Enter your text:")
    if st.button("text_to_audio_convert"):
        payload = {"inputs": text}
        audio_bytes = query(payload)
        # Play audio using Streamlit
        st.audio(audio_bytes, format="audio/wav")
        # Add a download button for the audio
        st.download_button("Download Audio", audio_bytes, file_name="output_audio.wav", key="download_audio")
        
# text_to_flag

def Text_to_flag():
    st.header("Text to flag")
    API_URL = "https://flagsapi.com/PK/flat/64.png"
    headers = {"Authorization": "Bearer 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"}
    
    # input text area
    user_input = st.text_area("Enter your country name:")

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    if st.button("Generate Response"):
        try:
            payload = {"inputs": user_input}
            result = query(payload)
            st.image(API_URL, caption='Generated Flag', use_column_width=True)
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
            st.text("Error occurred while generating the flag.")
# Text to image
def Text_to_img():
    st.header("Text_to_img")
    
    # input text area
    user_input = st.text_area("Enter your text:") 
    if st.button("Generate Image"):
        try:
            # Use the Robohash API to generate an image based on the text
            api_url = f"https://robohash.org/{user_input}.png"
            response = requests.get(api_url)

            if response.status_code == 200:
                st.image(response.content, caption='Generated Image', use_column_width=True)
            else:
                st.error(f"Failed to generate image. API returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
            st.text("Error occurred while generating the image.")
        

if __name__ == '__main__':
    main()

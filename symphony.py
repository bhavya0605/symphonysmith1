import streamlit as st
import base64
from transformers import pipeline
import scipy.io.wavfile

# Set page configuration
st.set_page_config(page_title="Symphony Smith", layout="wide")

# Cache the model using @st.cache_resource
@st.cache_resource
def load_model():
    return pipeline("text-to-audio", model="facebook/musicgen-small", device=0)

# Load the model only once
model = load_model()

# Session state to manage pages
if "page" not in st.session_state:
    st.session_state.page = "WelcomePage"
if "audio_data" not in st.session_state:
    st.session_state.audio_data = None
if "sampling_rate" not in st.session_state:
    st.session_state.sampling_rate = None

# Welcome page function
def welcome_page():
    with open('ssbg.jpg', "rb") as image_file:
        encoded_image_1 = base64.b64encode(image_file.read()).decode()

    st.markdown(f"""
                
        <style>
            .main {{
                background-image: url('data:image/jpeg;base64,{encoded_image_1}');
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
                color: white;
            }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>Welcome to Symphony Smith</h1>", unsafe_allow_html=True)
    go_button = st.button("Go Ahead")

    if go_button:
        st.session_state.page = "MainPage"

# Main page function
def main_page():
    with open('ssbg.jpg', "rb") as image_file:
        encoded_image_2 = base64.b64encode(image_file.read()).decode()

    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded_image_2}");
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Streamlit app
    st.title("Symphony Smith")
    prompt = st.text_input("Enter your music prompt:")

    if st.button("Generate Music"):
        if prompt:
            with st.spinner("Generating music..."):
                music = model(prompt, forward_params={"do_sample": True})
                audio_data = music["audio"]
                sampling_rate = music["sampling_rate"]

                # Save the generated music to a file
                output_file = "generated_music.wav"
                scipy.io.wavfile.write(output_file, rate=sampling_rate, data=audio_data)

                st.success("Music generated successfully!")
                st.audio(output_file, format="audio/wav")
        else:
            st.warning("Please enter a prompt to generate music.")

    if st.button("Back"):
        st.session_state.page = "WelcomePage"
#Generated music page function
def generated_music_page():
    with open('bgimg2.jpg', "rb") as image_file:
        encoded_image_2 = base64.b64encode(image_file.read()).decode()
# Thank you page function
def thank_you_page():
    st.markdown("<h1>Thank You for Using Symphony Smith!</h1>", unsafe_allow_html=True)
# Page navigation
if st.session_state.page == "WelcomePage":
    welcome_page()
elif st.session_state.page == "MainPage":
    main_page()
elif st.session_state.page == "GeneratedMusicPage":
    generated_music_page()
elif st.session_state.page == "ThankYouPage":
    thank_you_page()

import streamlit as st
import base64
import torch
from transformers import pipeline
import scipy.io.wavfile
import os

# Set page configuration
st.set_page_config(page_title="Symphony Smith", layout="wide")

# Cache the model using @st.cache_resource
@st.cache_resource
def load_model():
    device = 0 if torch.cuda.is_available() else -1
    return pipeline("text-to-audio", model="facebook/musicgen-small", device=device)

# Load the model only once
model = load_model()

# Session state to manage pages
if "page" not in st.session_state:
    st.session_state.page = "WelcomePage"
if "audio_data" not in st.session_state:
    st.session_state.audio_data = None
if "sampling_rate" not in st.session_state:
    st.session_state.sampling_rate = None

# Function to handle image encoding
def get_encoded_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    else:
        st.error(f"Image file '{image_path}' not found.")
        return None

# Welcome page function
def welcome_page():
    encoded_image_1 = get_encoded_image('ssbg.jpg')
    if encoded_image_1:
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
    encoded_image_2 = get_encoded_image('ssbg.jpg')
    if encoded_image_2:
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

    st.title("Symphony Smith")
    prompt = st.text_input("Enter your music prompt:")

    if st.button("Generate Music"):
        if prompt:
            with st.spinner("Generating music..."):
                music = model(prompt, forward_params={"do_sample": True})
                audio_data = music["audio"]
                sampling_rate = music["sampling_rate"]

                # Store the generated music in session state
                st.session_state.audio_data = audio_data
                st.session_state.sampling_rate = sampling_rate

                # Save the generated music to a file
                output_file = "generated_music.wav"
                scipy.io.wavfile.write(output_file, rate=sampling_rate, data=audio_data)

                st.success("Music generated successfully!")
                st.session_state.page = "GeneratedMusicPage"
        else:
            st.warning("Please enter a prompt to generate music.")

    if st.button("Back"):
        st.session_state.page = "WelcomePage"

# Generated music page function
def generated_music_page():
    st.title("Generated Music")
    if st.session_state.audio_data is not None and st.session_state.sampling_rate is not None:
        st.audio(st.session_state.audio_data, format="audio/wav")
    else:
        st.warning("No music generated yet. Please go back and generate music.")

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

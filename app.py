import streamlit as st
import pickle
import numpy as np
import base64
import gdown
import os

st.set_page_config(page_title="🔋 Wind Power Forecasting", layout="centered")

# Function to add background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-attachment: fixed;
        }}
        * {{
            color: white !important;
        }}
        .prediction-box {{
            background-color: black;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            font-size: 20px;
            color: white !important;
        }}
        .stTextInput input, .stNumberInput input, .stSelectbox div div div {{
            color: white !important;
            background-color: rgba(0, 0, 0, 0.6) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("background.jpg")

st.title("⚡ Wind Power Generation Forecasting")

# Google Drive file download
file_id = "1v8JTuZfPDn-N0sXfIPpoIRSA5lR82OG6"
output_path = "windpower.sav"

if not os.path.exists(output_path):
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output_path, quiet=False)

# Load model and scaler
with open(output_path, "rb") as file:
    data = pickle.load(file)

model = data['model']
scaler = data['scaler']

st.subheader("📊 Enter Weather Parameters")

col1, col2 = st.columns(2)

with col1:
    dew_point = st.number_input("🧊 Dew Point (°C)", value=10.0)
    windspeed_10m = st.number_input("🌬️ Wind Speed at 10m (m/s)", value=5.0)
    windspeed_100m = st.number_input("🌪️ Wind Speed at 100m (m/s)", value=7.0)
    wind_dir_10m = st.number_input("🧭 Wind Direction at 10m (°)", value=180.0)
    temperature = st.slider("🌡️ Temperature (°C)", 0.0, 50.0, 25.0)
    humidity = st.slider("💧 Humidity (%)", 0, 100, 60)

with col2:
    wind_dir_100m = st.number_input("🧭 Wind Direction at 100m (°)", value=200.0)
    gusts_10m = st.number_input("💨 Wind Gusts at 10m", value=10.0)
    hour = st.number_input("🕓 Hour of Day", 0, 23, 12)
    month = st.number_input("🗓️ Month", 1, 12, 6)

    location = st.selectbox("📍 Location", ['Location1', 'Location2', 'Location3', 'Location4'])
    loc2 = 1 if location == 'Location2' else 0
    loc3 = 1 if location == 'Location3' else 0
    loc4 = 1 if location == 'Location4' else 0

# Prepare input
input_data = [[
    temperature, humidity, dew_point, windspeed_10m, windspeed_100m,
    wind_dir_10m, wind_dir_100m, gusts_10m,
    loc2, loc3, loc4, hour, month
]]

scaled_input = scaler.transform(input_data)

# Predict and display result
if st.button("🚀 Predict Power Output"):
    prediction = model.predict(scaled_input)
    st.markdown(
        f'<div class="prediction-box">⚡ Predicted Wind Power Output: <b>{prediction[0]:.2f} MW</b></div>',
        unsafe_allow_html=True
    )

st.markdown("---")
st.markdown("<center>🔧 Made with ❤️ by Nidhi Sharma | ⚡ Model Accuracy: 72% </center>", unsafe_allow_html=True)

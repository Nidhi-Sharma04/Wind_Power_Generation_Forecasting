import streamlit as st
import numpy as np
import pickle
import base64

# Load model and scaler
with open("windpower.sav", "rb") as f:
    data = pickle.load(f)
    model = data["model"]
    scaler = data["scaler"]

# Page config
st.set_page_config(page_title="Wind Power Predictor", layout="centered")

# Background video with blur effect
def set_background_video(video_path):
    with open(video_path, "rb") as f:
        video_data = f.read()
        encoded = base64.b64encode(video_data).decode()

        st.markdown(f"""
        <style>
        html, body {{
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }}
        .video-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -2;
            overflow: hidden;
        }}
        .video-bg video {{
            object-fit: cover;
            width: 100%;
            height: 100%;
            filter: blur(3.5px);  /* Slight blur only */
        }}
        .stApp {{
            background: transparent;
        }}

        .title-box {{
            background-color: white;
            padding: 1.2rem 2rem;
            border-radius: 12px;
            text-align: center;
            font-size: 2.6rem;
            font-weight: 800;
            color: #111;
            margin: 3rem auto 2rem auto;
            max-width: 800px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}

        label, p, h3 {{
            color: #111 !important;
            font-weight: 500;
        }}

        div.stButton > button:first-child {{
            background-color: #f1f1f1;
            color: black;
            font-weight: 600;
            padding: 0.6rem 1.4rem;
            border: white;
            border-radius: 10px;
            transition: 0.3s ease;
        }}
        div.stButton > button:first-child:hover {{
            background-color: #f1f1f1;
            color:#111;
        }}
        </style>

        <div class="video-bg">
            <video autoplay muted loop>
                <source src="data:video/mp4;base64,{encoded}" type="video/mp4">
            </video>
        </div>
        """, unsafe_allow_html=True)

# Apply video background
set_background_video("background.mp4")

# ✅ Heading with white background
st.markdown('<div class="title-box">⚡ Wind Power Generation</div>', unsafe_allow_html=True)
st.write("Enter the weather and location details below to predict wind energy output.")

# Inputs directly floating over blurred background
col1, col2, col3 = st.columns(3)
with col1:
    temperature_2m = st.number_input("🌡️ Temperature at 2m (°C)", value=25.0)
    windspeed_10m = st.number_input("💨 Wind Speed at 10m (m/s)", value=3.0)
    winddirection_10m = st.number_input("🧭 Wind Direction at 10m (°)", value=150.0)
with col2:
    relativehumidity_2m = st.number_input("💧 Relative Humidity (%)", value=75.0)
    windspeed_100m = st.number_input("🌬️ Wind Speed at 100m (m/s)", value=6.0)
    winddirection_100m = st.number_input("🧭 Wind Direction at 100m (°)", value=160.0)
with col3:
    dewpoint_2m = st.number_input("❄️ Dew Point at 2m (°C)", value=10.0)
    windgusts_10m = st.number_input("🌪️ Wind Gusts at 10m (m/s)", value=5.0)

# Location input
st.markdown("### 📍 Select Windmill Location")
location = st.selectbox("Choose location CSV", ["Location1.csv", "Location2.csv", "Location3.csv", "Location4.csv"])
loc_2 = 1 if location == "Location2.csv" else 0
loc_3 = 1 if location == "Location3.csv" else 0
loc_4 = 1 if location == "Location4.csv" else 0

# Final input
input_data = [[
    temperature_2m, relativehumidity_2m, dewpoint_2m,
    windspeed_10m, windspeed_100m,
    winddirection_10m, winddirection_100m,
    windgusts_10m, loc_2, loc_3, loc_4
]]

# Prediction button
if st.button("💡 Predict Wind Power Output"):
    try:
        scaled = scaler.transform(input_data)
        result = model.predict(scaled)
        st.success(f"🔋 Predicted Output: **{result[0]:.2f} MW**")
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")

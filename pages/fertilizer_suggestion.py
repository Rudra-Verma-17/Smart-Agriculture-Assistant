import streamlit as st
import numpy as np
import os
import joblib

# Load model with error handling
model_path = os.path.join(os.path.dirname(__file__), "../fer_model.pkl")

try:
    if not os.path.exists(model_path):
        st.error("❌ Model file not found. Make sure 'fer_model.pkl' exists in the app root directory.")
        st.stop()

    model = joblib.load(model_path)

except ModuleNotFoundError:
    st.error("❌ Required library is missing. Try installing `scikit-learn`.")
    st.code("pip install scikit-learn")
    st.stop()

except Exception as e:
    st.error(f"❌ Failed to load model: {str(e)}")
    st.stop()

# Label dictionary
fer_dic = {
    0: 'Urea',
    1: 'DAP',
    2: '14-35-14',
    3: '28-28',
    4: '17-17-17',
    5: '20-20',
    6: '10-26-26'
}

# Fertilizer descriptions
fertilizer_description = {
    'Urea': 'Urea contains 46% nitrogen and is ideal for promoting leafy growth and green color in crops. Best used in early stages of crop growth.',
    'DAP': 'Diammonium phosphate (DAP) contains both nitrogen (18%) and phosphorus (46%). Encourages root development and early plant growth.',
    '14-35-14': 'This balanced fertilizer supports flowering and root development. Suitable for phosphorus-deficient soils.',
    '28-28': 'Used for balanced nitrogen and phosphorus needs, especially during early plant growth.',
    '17-17-17': 'A general-purpose fertilizer with balanced NPK ratios, ideal for maintaining overall plant health.',
    '20-20': 'Supports balanced vegetative and root growth. Useful for crops needing medium levels of nutrients.',
    '10-26-26': 'High in phosphorus and potassium, suitable for flowering and fruiting stages.'
}

# Options
soil_types = ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey']
crop_types = ['Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Barley', 'Wheat', 'Oil seeds', 'Pulses', 'Ground Nuts']

# Streamlit UI
st.set_page_config(page_title="Rudra | Fertilizer Recommendation", layout="centered")
st.title("🧪 Rudra Fertilizer Recommendation")
st.markdown("Enter environmental and crop details below to get the best fertilizer recommendation.")

# Input columns
col1, col2 = st.columns(2)

with col1:
    temperature = st.number_input("🌡️ Temperature (°C)", min_value=0.0, max_value=50.0)
    humidity = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0)
    moisture = st.number_input("🌱 Moisture (%)", min_value=0.0, max_value=100.0)
    soil = st.selectbox("🧱 Soil Type", soil_types)

with col2:
    crop = st.selectbox("🌿 Crop Type", crop_types)
    nitrogen = st.slider("🧪 Nitrogen Level", 0, 100)
    potassium = st.slider("🧪 Potassium Level", 0, 100)
    phosphorous = st.slider("🧪 Phosphorous Level", 0, 100)

soil_index = soil_types.index(soil)
crop_index = crop_types.index(crop)

st.markdown("---")

# Predict button
if st.button("🔍 Predict Fertilizer"):
    input_data = np.array([[temperature, humidity, moisture, soil_index, crop_index, nitrogen, potassium, phosphorous]])
    prediction = model.predict(input_data)[0]
    fertilizer = fer_dic.get(prediction, "Unknown")
    desc = fertilizer_description.get(fertilizer, "No description available.")

    st.markdown(f"""
        <div style="background-color:#014421;padding:14px 20px;border-radius:10px;color:white;margin-top:20px">
            ✅ <strong>Recommended Fertilizer:</strong> {fertilizer}<br>
            📘 <strong>Description:</strong> {desc}
        </div>
    """, unsafe_allow_html=True)

import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

st.set_page_config(page_title="Rudra | Disease Detection", layout="centered")

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="plant_disease_model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Class names
class_name = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
              'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
              'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
              'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
              'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
              'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
              'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
              'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
              'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
              'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
              'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
              'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
              'Tomato___healthy']

# Title
st.title("🌿 Rudra Crop Disease Detection")

# Upload section
uploaded_file = st.file_uploader("📤 Upload a leaf image", type=["jpg", "jpeg", "png"])

# Prediction function
def predict(image: Image.Image):
    image_resized = image.resize((128, 128))
    input_image = np.expand_dims(np.array(image_resized, dtype=np.float32), axis=0)
    input_image = tf.cast(input_image, input_details[0]['dtype'])

    interpreter.set_tensor(input_details[0]['index'], input_image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    result_index = np.argmax(output_data)
    confidence = output_data[0][result_index]
    disease_name = class_name[result_index]
    return disease_name, confidence

# Handle uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    disease_name, confidence = predict(image)
    st.subheader(f"🧪 Disease Prediction: `{disease_name}`")
    st.write(f"🔍 Confidence: `{confidence:.2f}`")

# Sample images
# Sample images
st.markdown("---")
st.subheader("📸 Try Sample Images")

sample_images = {
    "Potato - Early Blight": "PotatoEarlyBlight3.JPG",
    "Tomato - Yellow Curl Virus": "TomatoYellowCurlVirus3.JPG",
    "Apple - Cedar Rust": "AppleCedarRust1.JPG"
}

selected_sample = st.selectbox("Choose a sample image to test:", ["None"] + list(sample_images.keys()))

if selected_sample != "None":
    sample_path = sample_images[selected_sample]
    sample_image = Image.open(sample_path)
    st.image(sample_image, caption=selected_sample, use_container_width=True)

    # Show prediction only if not canceled
    if st.button("❌ Cancel Prediction"):
        st.warning("Prediction canceled.")
    else:
        disease_name, confidence = predict(sample_image)
        st.subheader(f"🧪 Prediction: `{disease_name}`")
        st.write(f"🔍 Confidence: `{confidence:.2f}`")

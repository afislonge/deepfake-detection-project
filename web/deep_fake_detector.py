import streamlit as st
from streamlit_extras.let_it_rain import rain
from PIL import Image
# import tensorflow as tf  
import random

# Logo path
logo_path = "Got U logo.jpg"

# Using column layout to center the logo
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.image(logo_path, use_column_width=True)

# Load your model (this is just an example path)
# model = tf.keras.models.load_model('path/to/your/model')

# This is a tempral code to test the web app
def classify_image(image):
    """Function to simulate classifying the image as real or fake."""
    # Simulate model prediction
    prediction = random.choice(['Real', 'Fake'])  # Randomly choose for simulation
    return prediction

# def classify_image(image):
#     """Function to classify the image as real or fake based on our model."""
    
#     # This is a temporary example of image tuning for the model:
#     img = image.resize((224, 224))  # Resize image to model's expected input size
#     img_array = tf.keras.preprocessing.image.img_to_array(img)
#     img_array = tf.expand_dims(img_array, 0)  # Create a batch

#     predictions = model.predict(img_array)
#     return predictions

# Streamlit app layout
st.title('Welcome to Got U: Your Go-To Deep Fake Image Detector 🕵🏻')
st.divider()

st.write("""
Navigating the digital world's real vs. fake landscape just got easier! With "Got U," you're one upload away from uncovering the truth behind any face image. 

**Why "Got U"?**

- **Spot the Real Deal**: Instantly find out if that image is genuine or a clever fake.
- **Simplicity is Key**: Our straightforward design means you get results fast, no tech wizardry required.
- **Join the Truth Squad**: Help us fight the good fight against digital deception by identifying deepfakes.
""")

st.write("""
**Your Voice Matters**

Got feedback? We're all ears! Your insights help us make "Got U" even better, ensuring we stay on the frontline of deepfake detection.
""")

st.write("😁 **Thanks for teaming up with Got U. Let's keep it real together!**")

st.divider()

st.subheader("Now, let's get into action...")
st.text("Please upload or drag and drop your image")

uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("Classifying...")
    
    prediction = classify_image(image)
    
    # Here the model will give the probability to make the prediction
    # 0.5 is an example, threshold can be adjusted
    # if prediction[0] > 0.5:  
    
    if prediction == "Fake":     
        st.error("The image is likely Fake ☹️👎🏻")
        rain(
        emoji="💀",
        font_size=40,
        falling_speed=3,
        animation_length=[5, 'seconds'], 
    )
    else:
        st.success("The image is likely Real 😁👍🏻")
        st.balloons()
        

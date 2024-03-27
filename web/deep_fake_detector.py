import streamlit as st
from streamlit_extras.let_it_rain import rain
from PIL import Image
import tensorflow as tf  
import random
from dotenv import load_dotenv, find_dotenv
import os 
from pymongo import MongoClient    

load_dotenv(find_dotenv())                      # load environment file to use password saved as an evironment var
password = os.environ.get("MONGODB_PWD")        # assing password store in env var

#connection string
MONGODB_URI = f"mongodb+srv://gotudeepfake:{password}@cluster0.jpdo5rg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGODB_URI)

db = client.deepfake                            # DataBase
collect = db.deepfake_report                     # Collection to stores counter for report

# Logo path
logo_path = "Got U logo.jpg"
fake_icon = "fake.png"
real_icon = "real.png"

placeholder = st.empty() #container

container = st.container()

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

def rezize_image(image):
    """Function to resize the image dimension."""
    img = image.resize((224, 224))  # Resize image to model's expected input size
    return img


def classify(image):

    #st.write("Classifying...")
    
    prediction = classify_image(image)
    
    # Here the model will give the probability to make the prediction
    # 0.5 is an example, threshold can be adjusted
    # if prediction[0] > 0.5:  
    
    if prediction == "Fake":     
    #     st.error("The image is likely Fake ☹️👎🏻")
    #     rain(
    #     emoji="💀",
    #     font_size=40,
    #     falling_speed=3,
    #     animation_length=[5, 'seconds'], 
    # )
        st.image(fake_icon,width=70)
        compute_report(0,1)

    else:
        #st.success("The image is likely Real 😁👍🏻")
        #st.balloons()
        st.image(real_icon,width=70)
        compute_report(1,0)
    
    
def compute_report(real, fake):   

    report  = collect.find_one()
    print(report)
    qry = { "_id": report["_id"] }

    submitted = int(report["number_submitted"]) + 1
    real_image_count = int(report["real_images_caught"]) + real
    fake_image_count = int(report["fake_images_caught"]) + fake

    colx1, colx2, colx3 = st.columns([1,1,1])
    with colx1:
        st.write("Number of time submitted")
        st.write(submitted)
    with colx2:
        st.write("Real images caught")
        st.write(real_image_count)
    with colx3:
        st.write("fake images caught")
        st.write(fake_image_count)

    deepfake_report= { "$set": {
        "number_submitted":submitted ,
        "real_images_caught":real_image_count,
        "fake_images_caught":fake_image_count
    }}

    collect.update_one(qry, deepfake_report, upsert=True)


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
    image_resize = rezize_image(image)
    col1, col2, col3 = st.columns([1,1,1])
    col1.empty()
    with col2:
        st.image(image_resize, caption='Uploaded Image')
        if st.button('Validate', type="primary"):
            classify(image_resize)
    col3.empty()

    
        

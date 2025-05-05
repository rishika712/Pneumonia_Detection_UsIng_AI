import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import sqlite3
import re
import os
import base64

# Set Streamlit page config
st.set_page_config(page_title="Pneumonia Detection", layout="centered")

# Database setup
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      username TEXT PRIMARY KEY, 
                      password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Load the ML model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model(r'C:\Users\RISHIKA\Downloads\pneumonia_model.h5')  # Update path if needed

model = load_model()

# Utility: Password validation
def is_valid_password(password):
    return (len(password) <= 12 and
            re.search(r"[A-Za-z]", password) and
            re.search(r"\d", password) and
            re.search(r"[^A-Za-z0-9]", password))

# Utility: Background styling
def set_background(image_file):
    with open(image_file, "rb") as img:
        b64_img = base64.b64encode(img.read()).decode()
        st.markdown(
            f"""<style>
            .stApp {{
                background-image: url("data:image/png;base64,{b64_img}"); 
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
            }}
            </style>""",
            unsafe_allow_html=True,
        )

# Image prediction
def predict(image):
    image = image.convert('RGB').resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model.predict(img_array)[0][0]
    return prediction

# Registration Page
def register():
    set_background("lung-banner.jpg")
    st.title("Register")
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    if st.button("Register", use_container_width=True):
        if not is_valid_password(password):
            st.markdown(
                "<div style='background-color:#f8d7da; color:#721c24; padding:10px; border-radius:8px;'>❌ Password must be ≤12 chars and include a letter, number, and special character.</div>",
                unsafe_allow_html=True)
        else:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                st.markdown(
                    "<div style='background-color:#d4edda; color:#155724; padding:10px; border-radius:8px;'>✅ Registration successful. You can now log in.</div>",
                    unsafe_allow_html=True)
                st.session_state.page = "login"
            except sqlite3.IntegrityError:
                st.markdown(
                    "<div style='background-color:#f8d7da; color:#721c24; padding:10px; border-radius:8px;'>❌ Username already exists.</div>",
                    unsafe_allow_html=True)
            conn.close()

# Login Page
def login():
    set_background("lung-banner.jpg")
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login", use_container_width=True):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.markdown(
                "<div style='background-color:#d1ecf1; color:#0c5460; padding:10px; border-radius:8px;'>🔐 Login successful!</div>",
                unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='background-color:#f8d7da; color:#721c24; padding:10px; border-radius:8px;'>❌ Incorrect username or password.</div>",
                unsafe_allow_html=True)

# Detection Page
def detection_page():
    set_background("lung-detection-bg.png")
    st.title("Pneumonia Detection")
    st.write("Upload a chest X-ray image:")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded X-ray", use_container_width=True)

        if st.button("Predict", use_container_width=True):
            with st.spinner("Analyzing..."):
                prediction = predict(image)
                if prediction > 0.5:
                    st.markdown(f"<h3 style='color:red; text-align:center;'>Pneumonia Detected (Confidence: {prediction:.2f})</h3>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h3 style='color:green; text-align:center;'>No Pneumonia Detected (Confidence: {1 - prediction:.2f})</h3>", unsafe_allow_html=True)

    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = "home"
        st.markdown(
            "<div style='background-color:#fff3cd; color:#856404; padding:10px; border-radius:8px;'>👋 Logged out successfully!</div>",
            unsafe_allow_html=True)

# Home Page
def home():
    set_background("lung-banner.jpg")
    st.title("🩺 Pneumonia Detection with AI")
    st.subheader("Smart Diagnosis from Chest X-rays")
    st.markdown("### Please choose an option below:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register", use_container_width=True):
            st.session_state.page = "register"
    with col2:
        if st.button("Login", use_container_width=True):
            st.session_state.page = "login"

# App Navigation
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.logged_in:
    detection_page()
else:
    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "register":
        register()
    elif st.session_state.page == "login":
        login()

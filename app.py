from dotenv import load_dotenv

load_dotenv() ## Load all env variables from .env file

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Funtion to load gemini pro vision
model=genai.GenerativeModel('gemini-pro-vision')

## Function to get response from gemini pro 
def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

## Function to get image details image data into bytes
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read file as bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaed.")



## Initialize the streamlit setup
st.set_page_config(page_title="Multi Language Invoice Processing")

st.header("Multi Language Invoice Processing")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Upload the image of invoice to be processed...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice", use_column_width=True)

submit=st.button("Extract requested information from invoice")

input_prompt="""
You are an expert in understanding invoices and extracting informatoin from it. We will upload an image as invoice and you will have to answer any questions related to the invoice based on the uploaded image.
"""

## If submit button is clicked
if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is: ")
    st.write(response)
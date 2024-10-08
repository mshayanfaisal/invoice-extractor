from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os 
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")

st.set_page_config(page_title = "AI-Powered Data Extraction and Automation")

st.header("AI-Powered Data Extraction and Automation")
input = st.text_input("Input Prompt: ", key= "input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp", ])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit =  st.button("Extract now")

input_prompt = """
You are an expert in understanding invoices. We will upload a image as invoice
and you will have to answer any question based on the uploaded invoice image. Extract key details such as invoice number, date, total amount, billing and shipping addresses, itemized list of products or services, and any applicable taxes or discounts. If the provided document is in some another language you should be capable of translating it into user desired language. 
"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is")
    st.write(response)
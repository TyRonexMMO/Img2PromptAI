import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure GenerativeAI with your API key
genai.configure(api_key="AIzaSyBZQmot8_8bDxuGiffJ06woJCzH140Erc4")

# Function to get response from GenerativeAI model
def get_response(input_text, input_image):
    # Initialize GenerativeAI model
    model = genai.GenerativeModel('gemini-pro-vision')
    try:
        # Generate content based on input text and/or image
        if input_text:
            input_sequence = [input_text]
            if input_image:
                input_sequence.append(input_image)
            response = model.generate_content(input_sequence)
        else:
            response = model.generate_content([input_image])
        return response.text
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Streamlit app header
st.title("GenerativeAI Chat")

# Input field for text prompt
input_text = st.text_input("Input prompt")

# File uploader for image
uploaded_image = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
selected_image = None
if uploaded_image is not None:
    selected_image = Image.open(uploaded_image)
    st.image(selected_image, caption='Uploaded Image', use_column_width=True)

# Button to submit request
submit_button = st.button('Generate')
if submit_button:
    if input_text or selected_image:
        with st.spinner("Generating..."):
            if selected_image is not None:
                # If both input text and image are provided
                response = get_response(input_text, selected_image)
                if response:
                    st.markdown("---")
                    st.subheader("Generated Response:")
                    st.info(response)
            elif input_text:
                # If only input text is provided
                response = get_response(input_text, None)
                if response:
                    st.markdown("---")
                    st.subheader("Generated Response:")
                    st.info(response)
    else:
        st.warning("Please provide input text or upload an image.")
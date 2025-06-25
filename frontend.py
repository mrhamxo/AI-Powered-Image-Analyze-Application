import streamlit as st
from PIL import Image
import requests

# Streamlit layout configuration to use full page width
st.set_page_config(layout="wide")

# API endpoint that connects to your FastAPI backend
API_URL = "http://127.0.0.1:8000/upload_and_query"

# Title of the app
st.title("AI-POWERED IMAGE ANALYZE APPLICATION")

# Create two side-by-side columns for upload and question input
col1, col2 = st.columns(2)

# -------------------- Column 1: Upload Image --------------------
with col1:
    upload_container = st.container(border=True)
    with upload_container:
        st.header("Upload Image")
        
        # Upload file input (jpg, jpeg, png)
        uploaded_file = st.file_uploader("Click to Upload", type=["jpg", "jpeg", "png"], 
                                         label_visibility="collapsed")
        
        # If an image is uploaded
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)

                # Resize the image to fixed dimensions for consistent display
                resized_image = image.resize((200, 80))  # Width: 200px, Height: 80px
                
                # Display the resized image in the container
                st.image(resized_image, caption="Image Uploaded", use_container_width=True)
            except:
                st.error("The uploaded file is not a valid image")

# -------------------- Column 2: Ask Question --------------------
with col2:
    question_container = st.container(border=True)
    with question_container:
        # Apply custom height to the container using CSS
        st.markdown(
            """
            <style>
                div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"] {
                    height: 500px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.header("Ask Question")
        
        # Text area for user to enter their query
        user_question = st.text_area(
            "Enter your question about the image",
            label_visibility="collapsed",
            height=200,
            placeholder="Type your medical question here..."
        )

        # Submit button
        submit_button = st.button("Submit Query")

# -------------------- Response Handling --------------------
if submit_button and user_question:
    st.markdown("---")  # Visual separator

    # Ensure that an image is uploaded before submitting
    if uploaded_file is None:
        st.error("⚠️ Please upload an image before submitting your query.")
    else:
        # Try sending the request to the backend API
        with st.spinner("Analyzing image..."):
            try:
                # Reset file pointer and read image bytes
                uploaded_file.seek(0)
                file_bytes = uploaded_file.read()
                
                # Prepare multipart form data
                files = {
                    "image": (uploaded_file.name, file_bytes, uploaded_file.type)
                }
                
                # Send POST request to FastAPI backend
                response = requests.post(
                    API_URL,
                    files=files,
                    data={"query": user_question},
                    timeout=30
                )

                # If successful, parse the responses
                if response.status_code == 200:
                    result = response.json()
                    llama_scout_response = result.get("llama Scout", "No response from Scout model.")
                    llama_maverick_response = result.get("llama Maverick", "No response from Maverick model.")
                else:
                    # Handle HTTP error
                    llama_scout_response = f"❌ Error: {response.status_code} - {response.text}"
                    llama_maverick_response = f"❌ Error: {response.status_code} - {response.text}"

            except Exception as e:
                # Catch and show general error
                llama_scout_response = "❌ Exception occurred while sending request."
                llama_maverick_response = str(e)

    # -------------------- Column 3: Scout Model Response --------------------
    col3, col4 = st.columns(2)

    with col3:
        response1_container = st.container(border=True)
        with response1_container:
            st.subheader("llama-4-scout-17b-16e-instruct Response")
            if uploaded_file is not None:
                st.write(llama_scout_response)
            else:
                st.write("Please upload an image first for analysis.")

    # -------------------- Column 4: Maverick Model Response --------------------
    with col4:
        response2_container = st.container(border=True)
        with response2_container:
            st.subheader("llama-4-maverick-17b-128e-instruct Response")
            if uploaded_file is not None:
                st.write(llama_maverick_response)
            else:
                st.write("Please upload an image first for analysis.")


# -------------------- Footer with Social Icons --------------------
st.markdown(
    """
    <hr style="border: 0.5px solid #6B7280; margin-top: 40px; margin-bottom: 10px;" />
    <div style='text-align: center; font-size: 14px; color: gray;'>
        Developed by <strong>Muhammad Hamza</strong> | Powered by <strong>Groq Multimodal LLMs</strong><br>
        Connect with me:
        <a href="https://github.com/mrhamxo" target="_blank" style="margin: 0 10px;">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" height="20px" />
        </a>
        <a href="https://www.linkedin.com/in/muhammad-hamza-khattak/" target="_blank" style="margin: 0 10px;">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" height="20px" />
        </a>
        <a href="mailto:mr.hamxa942@gmail.com" target="_blank" style="margin: 0 10px;">
            <img src="https://img.icons8.com/ios-filled/50/999999/email.png" height="20px" />
        </a>
        <br><br>© 2025 AI-POWERED. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)

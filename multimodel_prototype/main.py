import requests
import io
from PIL import Image
import base64
import os
from dotenv import load_dotenv
import logging

# Configure the logging system to show messages at INFO level or higher (INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(level=logging.INFO)

# Create a logger object specific to this module/file
# '__name__' ensures that the logger's name matches the current module's name
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Define the Groq API URL for multimodal chat completions
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Retrieve the Groq API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Raise an error if the API key is not set
if not GROQ_API_KEY:
    raise ValueError('GROQ_API_KEY is not set .env file')

def process_image(image_path, query):
    try:
        # Open the image file in binary read mode
        with open(image_path, "rb") as image_file:
            # Read the image data
            image_data = image_file.read()
            # Convert the binary image data to base64 string
            image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        try:
            # Attempt to open the image using PIL for additional processing or validation
            img = Image.open(io.BytesIO(image_data))
            img.verify()  # Verify that the image is valid and not corrupted
        
        except Exception as e:
            # Log error if the image cannot be opened
            logger.error(f"Error opening image: {str(e)}")
            return {"error": f"Error opening image: {str(e)}"}
        
        # Compose the multimodal message: one role=user message containing both text and image
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }
        ]
        
        # Function to send request to a given Groq model with messages
        def make_api_request(model):
            response = requests.post(
                GROQ_API_URL,
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 1000,
                },
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json" 
                },
                timeout=30  # Set a timeout for the request
            )
            return response
        
        # Call both Scout and Maverick models
        llama_scout_response = make_api_request("meta-llama/llama-4-scout-17b-16e-instruct")
        llama_maverick_response = make_api_request("meta-llama/llama-4-maverick-17b-128e-instruct")
        
        responses = {}  # Dictionary to hold results from each model
        for model, response in [("llama Scout", llama_scout_response), ("llama Maverick", llama_maverick_response)]:
            if response.status_code == 200:
                # Extract and store the answer from the model's response
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
                logger.info(f"Processed response from {model} API: {answer[:100]}...")
                responses[model] = answer
            else:
                # Log error if the API request fails
                logger.error(f"Error from {model} API: {response.status_code} - {response.text}")
                responses[model] = f"Error from: {model} API : {response.status_code}"        
        return responses
    
    except Exception as e:
        # Log any unexpected error (e.g., file not found, permission error)
        logger.error(f"An unexpected error occurred: {str(e)}")
        return {"error": f"An unexpected error occurred: {str(e)}"}

# This block ensures the code only runs when the script is executed directly,
# not when it's imported as a module in another script.
if __name__ == "__main__":
    
    # Path to the image you want to analyze
    image_path = "test1.png"
    
    # The question or query you want to ask about the image
    query = "what are the encoders in this picture?"
    
    # Call the function 'process_image' with the image and query
    # This function is expected to process the image and return a response from a vision model
    result = process_image(image_path, query)
    
    # Print the result returned by the model (e.g., a description or answer)
    print(result)

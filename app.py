from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn

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

app = FastAPI()

# Define the Groq API URL for multimodal chat completions
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Retrieve the Groq API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Raise an error if the API key is not set
if not GROQ_API_KEY:
    raise ValueError('GROQ_API_KEY is not set .env file')

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return JSONResponse(status_code=200, content={"message": "WELCOME TO THE AI-DOCTOR (MEDICAL CHATBOT) ANALYZE IMAGE APPLICATION API!"})

@app.post("/upload_and_query")
async def upload_and_query(image: UploadFile = File(...), query: str = Form(...)):
    try:
        image_data = await image.read()
        if not image_data:
            raise HTTPException(status_code=400, detail="Image file is empty")
        
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        try:
            # Attempt to open the image using PIL for additional processing or validation
            img = Image.open(io.BytesIO(image_data))
            img.verify()  # Verify that the image is valid and not corrupted
        
        except Exception as e:
            # Log error if the image cannot be opened
            logger.error(f"Invalid image format: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")
        
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
                answer = result["choices"][0]["message"].get("content", "⚠️ No content returned.")
                logger.info(f"Processed response from {model} API: {answer[:100]}...")
                responses[model] = answer
            else:
                # Log error if the API request fails
                logger.error(f"Error from {model} API: {response.status_code} - {response.text}")
                responses[model] = f"Error from: {model} API : {response.status_code}"        
                
        return JSONResponse(status_code=200, content=responses)
        
    except HTTPException as he:
        logger.error(f"HTTP Exception: {str(he)}")
        raise he
    
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
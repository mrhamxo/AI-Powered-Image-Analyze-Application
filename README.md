# 🧠 AI-Powered Image Analyze Application

A powerful multimodal AI web app built using **FastAPI**, **Streamlit**, and **Groq's LLaMA-4 Vision Models**. Upload a any image and ask natural language questions to receive insightful responses powered by state-of-the-art LLMs.

This app is built using:
- 🌐 FastAPI for high-performance backend processing
- 🎨 Streamlit for an intuitive and responsive frontend
- ⚡ Groq’s multimodal LLaMA-4 models for powerful image+text understanding

## 🚀 APP Demo

![Image](https://github.com/user-attachments/assets/b4324249-b179-4913-8e9e-64f304ca8b7e)
![Image](https://github.com/user-attachments/assets/6f3ca962-f71c-4d52-a842-e05837901319)

## 🧩 Features

- 🖼️ Upload any image such as **medical or clinical image**
- 💬 Ask **natural language questions** about the image
- 🤖 Get answers from two **Groq multimodal models**:
  - `llama-4-scout-17b-16e-instruct`
  - `llama-4-maverick-17b-128e-instruct`
- ⚡ Built for **fast, local testing and deployment**
- 🎨 Modern **Streamlit UI** with Tailwind-style responsiveness
- 🔐 Secure API integration using **.env**.

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-doctor-app.git
cd ai-doctor-app
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your `.env` file

```env
# .env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the FastAPI backend

```bash
uvicorn app:app --reload
# Running on http://127.0.0.1:8000
```

### 6. In a new terminal, launch the frontend

```bash
streamlit run frontend.py
```

## 🔌 API Endpoint

```http
POST /upload_and_query
```

**Payload**:

* `image` (form-data): Image file
* `query` (form-data): User's natural language question

**Returns**:

```json
{
  "llama Scout": "Response from Scout model...",
  "llama Maverick": "Response from Maverick model..."
}
```

## 💡 Sample Prompts

* "What type of tumor is visible in this image?"
* "Are there signs of pneumonia in the scan?"
* "What are the encoders in this architecture diagram?"

## 👨‍💻 Author

**Muhammad Hamza**
💼 [LinkedIn](https://linkedin.com/in/your-linkedin)
💻 [GitHub](https://github.com/mrhamxo)
📬 [Email](mailto:mr.hamxa942@gmail.com)

## 📝 License

This project is licensed under the **MIT License**.
Feel free to fork, modify, and contribute!

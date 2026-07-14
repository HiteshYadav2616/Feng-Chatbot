# 🎓 Feng – AI Chatbot

Feng is an AI-powered chatbot built with **Streamlit**, **LangChain**, and **Groq's Llama 3.3 70B Versatile** model. It provides a clean chat interface with support for multiple conversations, chat history, and an intuitive sidebar for managing chats.

---

## 🚀 Features

* 💬 Interactive AI chatbot
* 🧠 Conversational memory within each chat
* 📂 Multiple chat sessions
* ➕ Create new conversations
* 🗑️ Delete individual chats
* 🧹 Clear the current conversation
* ⚡ Fast responses using Groq's Llama 3.3 70B Versatile model
* 🎨 Modern Streamlit interface

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* Groq API
* python-dotenv

---

## 📁 Project Structure

```text
Feng/
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
└── ...
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/HiteshYadav2616/Feng-Chatbot.git
cd Feng-Chatbot
```

### 2. Create a virtual environment

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

> **Note:** Never upload your `.env` file to GitHub.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## 📌 Future Improvements

* Chat history persistence using a database
* User authentication
* File upload and document Q&A (RAG)
* Voice input and output
* Chat export
* Dark mode
* Streaming responses
* Docker support
* Cloud deployment

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Hitesh**

If you found this project useful, consider giving it a ⭐ on GitHub.

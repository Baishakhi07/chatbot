# 🌿 HR GreenBot – Your Streamlit-Powered HR Assistant

**HR GreenBot** is a stylish, eco-themed chatbot built with [Streamlit](https://streamlit.io) and powered by a local large language model (via [Ollama](https://ollama.com/)). It offers a warm, modern interface designed to support HR queries like checking leave balance, onboarding progress, and payroll questions.

![screenshot](https://your-screenshot-url-here.com)

---

## ✨ Features

- 🎨 Beautiful caramel-toned modern UI with Poppins font and soft shadows
- 🤖 Local AI responses via [Mistral](https://ollama.com/library/mistral) or compatible models
- 💬 Chat bubbles for user and bot with animated typing indicators
- 🧾 Fully interactive interface with session tracking
- 🔐 Runs locally, no cloud dependencies or API keys required

---

## 🛠 Requirements

- Python 3.9+
- Streamlit
- Ollama (running locally with a model like `mistral`)

---

## 🚀 Getting Started

1. **Clone the repo**

```bash
git clone https://github.com/your-username/hr-greenbot.git
cd hr-greenbot

## Install dependencies:
pip install -r requirements.txt

## Start Ollama with a model
ollama run mistral

## Run the app
streamlit run gui.py


## Project structure
.
├── gui.py              # Main Streamlit app
├── chatbot.py          # Optional CLI interface
├── requirements.txt
└── README.md


🙌 Acknowledgements
Ollama

Streamlit

Poppins Font


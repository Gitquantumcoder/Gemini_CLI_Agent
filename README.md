<div align="center">

# ⚡🐹 Pikachu an AI Agent ⚡

### A terminal-based conversational AI agent powered by Google's Gemini API

*Chat, analyze images, and generate pictures — all from your command line.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Gemini API](https://img.shields.io/badge/Powered%20by-Gemini%20API-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](#license)

</div>

---

## 📖 Overview

**Pikachu** is a lightweight, configurable command-line agent built on top of Google's `google-genai` SDK. It supports natural conversation with memory, image understanding (vision), and on-demand image generation — all wrapped in a friendly, electric-themed CLI experience.

This project was built as a hands-on exploration of **agentic AI design**: persona customization, prompt injection for response formatting, multimodal I/O, and lightweight conversational memory management.

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **Conversational Memory** | Remembers the full chat history within a session and feeds it back as context on every turn |
| 🖼️ **Image Analysis** | Attach an image (`.jpg`, `.png`, `.webp`, `.gif`, `.bmp`, `.tiff`, `.heic`, `.heif`) and ask questions about it |
| 🎨 **Image Generation** | Trigger phrases like *"generate an image of..."* create and save a picture automatically |
| 🎭 **Custom Persona** | Define the agent's personality and tone via a `--system` prompt flag |
| 🌡️ **Adjustable Creativity** | Control response randomness with a `--temperature` flag (0 = factual, 2 = highly creative) |
| ✂️ **Concise Replies** | Built-in formatting rules keep responses short, line-wrapped, and free of filler |
| 📋 **Session Commands** | View (`history`), reset (`clear`), or exit (`exit`) the conversation at any time |

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **AI Backend:** Google Gemini API (`google-genai`)
- **Models used:** `gemini-3.5-flash` (text), `gemini-2.5-flash-image` (image generation), `gemini-2.5-flash` (vision)
- **Config:** `python-dotenv` for environment variable management

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/pikachu-ai-agent.git
   cd pikachu-ai-agent
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install google-genai python-dotenv
   ```

4. **Set up your API key**

   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

   Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## 🚀 Usage

Run the agent with default settings:

```bash
python gemini_agent.py
```

### Optional flags

```bash
python gemini_agent.py --temperature 1.2 --system "You are a witty pirate assistant."
```

| Flag | Description | Default |
|---|---|---|
| `--temperature` | Creativity level (0.0 – 2.0) | `0.7` |
| `--system` | Custom system prompt / persona | *"You are a helpful, friendly AI assistant."* |

### In-session commands

| Command | Action |
|---|---|
| `history` | Show the full conversation memory |
| `clear` | Wipe the current memory |
| `exit` | Quit the agent |

### Example session

```
You: What's the capital of Japan?
⚡🐹 Pikachu: Tokyo is the capital of Japan.

You: generate an image of a cat riding a skateboard
⚡🐹 [Pikachu] Image generation request → Imagen 3...
✅ Saved image → 'generated_image_1.jpg'

You: (attach an image to analyze it when prompted)
```

---

## 📂 Project Structure

```
pikachu-ai-agent/
├── gemini_agent.py     # Main agent script
├── .env                # API key (not committed)
└── README.md
```

---

## 🗺️ Roadmap

- [ ] Persistent memory across sessions (file/DB-backed)
- [ ] Streaming responses for faster perceived latency
- [ ] Web UI wrapper (FastAPI / Streamlit)
- [ ] Multi-turn image editing support

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues) or open a pull request.

---

Author- Mohd.Afzal
B.tech-CSE
Specialization in AI/ML

---
## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Made with ⚡ and a lot of *Pika pika*

</div>

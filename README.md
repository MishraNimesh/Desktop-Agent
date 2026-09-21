# AI Desktop Agent

## Overview

A lightweight Windows desktop utility that provides a context‑aware AI assistant. The assistant can be summoned from anywhere via a global keyboard shortcut (default **Ctrl + Shift + Space**) and offers two primary modes:

1. **Screen** – Capture the current screen, ask a question, and get an answer from the Gemini multimodal model.
2. **Doodle** – (Future) Draw on a transparent overlay, capture the doodle, and ask the AI.

The first release implements **Phase 1** – global hotkey, launcher UI, screen capture, Gemini integration, and response display.

---

## Features (Phase 1)

- Runs in the background and listens for a global hotkey.
- Small floating launcher with a **Screen** button.
- Captures the primary monitor screenshot.
- Prompts the user for a question.
- Sends the image + question to the Gemini API.
- Shows the AI response in a floating window.
- Dark theme, modern minimal UI using **PySide6**.

---

## Project Structure

```
ai-desktop-agent/
│
├─ app/
│   ├─ main.py            # Entry point, hotkey registration
│   ├─ config.py          # Configuration (environment loading)
│   ├─ hotkey.py          # Global shortcut handling
│   ├─ screen_capture.py  # Screenshot utilities
│   ├─ gemini_client.py   # Gemini API wrapper
│   ├─ overlay.py         # Base overlay utilities (future use)
│   ├─ launcher.py        # Launcher UI (Screen button)
│   ├─ doodle.py          # Doodle overlay (Phase 2)
│   └─ response_window.py# Response display UI
│
├─ assets/                # Optional static assets (icons, etc.)
│
├─ .env.example           # Template for environment variables
├─ .gitignore             # Ignored files
├─ requirements.txt       # Python dependencies
└─ README.md              # This file
```

---

## Setup Instructions

1. **Python version** – Requires Python 3.9+ (tested on 3.11).
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # on Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure the Gemini API key**:
   - Copy `.env.example` to `.env`.
   - Replace `your_gemini_api_key_here` with your actual Gemini API key.
   - **Never commit** `.env` – it is already listed in `.gitignore`.
5. **Run the application**:
   ```bash
   python app/main.py
   ```
   The app runs in the background and listens for the hotkey.

---

## Usage

- Press **Ctrl + Shift + Space** to open the launcher.
- Click **Screen**.
- A prompt appears – type your question about the captured screen.
- The AI's answer shows in a floating response window.
- Press **Esc** to dismiss any overlay.

---

## Limitations (Phase 1)

- Only captures the primary monitor.
- Doodle mode is not yet implemented.
- No system‑tray icon (planned for Phase 3).
- Error messages are shown as simple dialogs.

---

## Future Roadmap

- **Phase 2** – Add Doodle mode with drawing tools.
- **Phase 3** – System tray integration, animations, better styling.
- **Phase 4** – Multi‑monitor support, region selection, active‑window capture, conversation history, provider‑agnostic AI layer.

---

## Contributing

Feel free to open issues or submit pull requests. Keep the architecture modular so the AI provider can be swapped out without touching the UI code.

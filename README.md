# Voice-Powered Language Translator

A beginner-friendly desktop app for translating spoken or typed text between dozens of languages, powered by local AI (Ollama Llama 3.2) and a simple, beautiful interface.

---

## Features
- Speak or type to translate between 30+ languages
- Simple, modern, and accessible UI
- Visual timer while recording
- Clear status feedback (Ready, Recording, Processing, Error, Done)
- All actions (Record, Stop, Clear, Translate) are one-click
- No internet required for translation (uses local Ollama model)
- Logs all sessions for review

---

## Prerequisites

### 1. Python 3.8+
- [Download Python](https://www.python.org/downloads/)

### 2. Required Python Packages
- `speech_recognition`
- `requests`
- `tkinter` (comes with most Python installations)
- `pyaudio` (for microphone input)

Install them with:
```sh
pip install speechrecognition requests pyaudio
```

#### On macOS, you may need PortAudio:
```sh
brew install portaudio
pip install pyaudio
```

### 3. Ollama (for local AI translation)
- [Install Ollama](https://ollama.com/download)
- Pull the Llama 3.2 model:
```sh
ollama pull llama3.2
```
- Start the Ollama server:
```sh
ollama serve
```

---

## How to Run the App
1. Make sure Ollama is running (`ollama serve` in a terminal).
2. In another terminal, run:
```sh
python langAssist.py
```

---

## Usage Instructions
1. **Select source and target languages** from the dropdowns.
2. **To speak:**
   - Click **Record** and speak your phrase.
   - Click **Stop** when finished.
   - The app will transcribe and translate your speech.
3. **To type:**
   - Type your text in the **Transcript** box.
   - Click **Translate**.
4. **Clear** resets everything for a new translation.
5. The **Translation** box will show your result.
6. The status bar at the bottom shows what the app is doing.

---

## Troubleshooting
- **Microphone not working?**
  - Make sure your mic is plugged in and not muted.
  - On macOS, you may need to grant Terminal or Python access to the microphone in System Settings > Privacy & Security > Microphone.
  - If you see a PortAudio error, install it with `brew install portaudio` (macOS) and reinstall `pyaudio`.
- **Ollama errors?**
  - Make sure you have run `ollama serve` and pulled the `llama3.2` model.
  - The app must be able to connect to `http://localhost:11434`.
- **Buttons require a hard click?**
  - Enable "Tap to click" in your Mac's Trackpad settings.
- **App looks weird or text is missing?**
  - Make sure you are running Python 3.8+ and have all dependencies installed.

---

## Example Screenshots
*(Add screenshots here after running the app!)*

---

## Credits
- Built with [Tkinter](https://docs.python.org/3/library/tkinter.html), [SpeechRecognition](https://pypi.org/project/SpeechRecognition/), [Ollama](https://ollama.com/), and [Llama 3.2](https://ollama.com/library/llama3.2).

---

## Highly Specific Prompt for GPT-4o to Replicate This App

**Prompt:**

> Build a Python desktop app using Tkinter called "Voice-Powered Language Translator" with the following requirements:
>
> 1. **Language Selection:**
>    - Provide two dropdown menus at the top: one for "Translate from" and one for "Translate to".
>    - Include at least 30 languages (e.g., English, Spanish, French, German, Chinese, Japanese, etc.).
>    - Prevent the user from selecting the same language for both dropdowns (show a warning if attempted).
>
> 2. **Input Methods:**
>    - Allow the user to either:
>      - Click a large, clearly labeled **Record** button to start recording speech from the microphone, and a **Stop** button to end recording (no auto-stop; only user stops it).
>      - Or type directly into a large, editable **Transcript** text area.
>
> 3. **Visual Timer:**
>    - While recording, display a timer (in seconds) in the status bar, updating every second.
>
> 4. **Translation:**
>    - After recording, automatically transcribe the speech and place it in the Transcript box.
>    - Provide a large, clearly labeled **Translate** button that translates the text in the Transcript box (whether typed or transcribed).
>    - Show the translation in a large, read-only **Translation** text area below.
>
> 5. **UI/UX:**
>    - Use a modern, light color palette: light backgrounds, dark text, and visually distinct, color-coded status bar (e.g., green for Ready, yellow for Recording, blue for Processing, red for Error, purple for Done).
>    - All buttons (Record, Stop, Clear, Translate) should be large, touch-friendly, and have high-contrast text.
>    - Add a **Clear** button to reset both text areas and the status bar.
>    - Add clear, beginner-friendly instructions at the top of the window.
>    - Make the window and text areas resizable.
>
> 6. **Status Bar:**
>    - Show a persistent status bar at the bottom with color-coded feedback: Ready, Recording, Processing, Error, Done.
>
> 7. **AI Integration:**
>    - Use the local Ollama Llama 3.2 model for translation by sending a POST request to `http://localhost:11434/api/generate` with the following JSON:
>      ```json
>      {"model": "llama3.2", "prompt": "Translate from [FROM] to [TO]: [TEXT]", "stream": false}
>      ```
>    - Extract the translation from the `response` field of the returned JSON.
>    - Handle connection errors gracefully (show a user-friendly error message if Ollama is not running).
>
> 8. **Logging:**
>    - Log each session (transcript, prompt, translation) to a timestamped text file in a `logs/` folder.
>
> 9. **Dependencies:**
>    - Only require Python, Tkinter, SpeechRecognition, requests, pyaudio, and Ollama (with Llama 3.2 model).
>
> 10. **Error Handling:**
>     - Show clear, user-friendly error messages for microphone issues, API errors, or invalid input.
>     - Prevent the app from crashing on any user action.
>
> 11. **Accessibility:**
>     - Ensure all text is readable (large font, high contrast).
>     - All actions should be accessible by mouse or touch (no keyboard required).
>
> 12. **Beginner-Friendliness:**
>     - The app should be easy to use for someone with no programming experience.
>     - Include clear instructions and feedback for every action.
>
> 13. **General:**
>     - The app should be robust, visually appealing, and require no internet connection for translation.
>     - The code should be clean, well-commented, and easy to follow.

--- 
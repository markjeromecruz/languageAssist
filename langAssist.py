import speech_recognition as sr
import requests
import tkinter as tk
from tkinter import messagebox
import datetime
import os
import threading

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        root.title("Voice-Powered Language Translator")
        root.geometry("600x600")
        root.minsize(500, 500)

        # Set a modern, light background for the main window
        root.configure(bg="#f4f6fb")

        # Instructions
        instructions = (
            "Instructions:\n"
            "1. Select languages.\n"
            "2. Press Record, speak, then Stop.\n"
            "3. Or type in the transcript box and press Translate."
        )
        tk.Label(root, text=instructions, justify=tk.LEFT, font=("Arial", 11, "bold"), bg="#f4f6fb", fg="#22223b").pack(pady=6)

        # Initialize recognizer
        self.recognizer = sr.Recognizer()

        # Attempt to initialize microphone, handle missing PyAudio dependency
        try:
            self.mic = sr.Microphone()
        except AttributeError:
            messagebox.showerror(
                "Dependency Error",
                "PyAudio is not installed or PortAudio is missing.\n"
                "On macOS, install PortAudio and PyAudio: brew install portaudio && pip install pyaudio"
            )
            root.destroy()
            return

        # Language selection (FROM and TO)
        languages = [
            "English", "Spanish", "French", "German", "Italian", "Portuguese", "Dutch",
            "Russian", "Chinese (Simplified)", "Chinese (Traditional)", "Japanese", "Korean",
            "Arabic", "Hebrew", "Hindi", "Polish", "Turkish", "Greek", "Swedish", "Danish",
            "Norwegian", "Finnish", "Hungarian", "Romanian", "Ukrainian", "Czech", "Bulgarian",
            "Serbian", "Croatian", "Slovak", "Estonian", "Latvian", "Lithuanian", "Belarusian"
        ]
        self.from_lang_var = tk.StringVar(value=languages[0])
        self.to_lang_var = tk.StringVar(value=languages[1])
        lang_frame = tk.Frame(root, bg="#f4f6fb")
        lang_frame.pack(pady=4)
        tk.Label(lang_frame, text="Translate from:", bg="#f4f6fb", fg="#22223b").pack(side=tk.LEFT, padx=2)
        from_menu = tk.OptionMenu(lang_frame, self.from_lang_var, *languages, command=self._prevent_same_lang)
        from_menu.config(bg="#e9ecef", fg="#22223b", font=("Arial", 11))
        from_menu.pack(side=tk.LEFT)
        tk.Label(lang_frame, text="to:", bg="#f4f6fb", fg="#22223b").pack(side=tk.LEFT, padx=2)
        to_menu = tk.OptionMenu(lang_frame, self.to_lang_var, *languages, command=self._prevent_same_lang)
        to_menu.config(bg="#e9ecef", fg="#22223b", font=("Arial", 11))
        to_menu.pack(side=tk.LEFT)

        # Buttons
        button_frame = tk.Frame(root, bg="#f4f6fb")
        button_frame.pack(pady=10)
        btn_style = {'width': 16, 'height': 2, 'font': ("Arial", 12, "bold"), 'bg': '#e9ecef', 'fg': '#22223b', 'activebackground': '#b5c1d8', 'activeforeground': '#22223b', 'relief': tk.RAISED, 'bd': 3, 'cursor': 'hand2'}
        self.record_button = tk.Button(button_frame, text="Record", command=self.start_recording, **btn_style)
        self.record_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.stop_button = tk.Button(button_frame, text="Stop", state=tk.DISABLED, command=self.stop_recording, **btn_style)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_text, **btn_style)
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.translate_button = tk.Button(button_frame, text="Translate", command=self.manual_translate, **btn_style)
        self.translate_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Transcript and Feedback text areas
        tk.Label(root, text="Transcript:", bg="#f4f6fb", fg="#22223b").pack()
        self.transcript_text = tk.Text(root, height=7, wrap=tk.WORD, bg="#f8f9fa", fg="#22223b", font=("Arial", 12), insertbackground="#22223b")
        self.transcript_text.pack(padx=8, pady=4, fill=tk.BOTH, expand=True)
        self.transcript_text.bind("<KeyRelease>", lambda e: self._auto_scroll(self.transcript_text))
        tk.Label(root, text="Translation:", bg="#f4f6fb", fg="#22223b").pack()
        self.feedback_text = tk.Text(root, height=7, wrap=tk.WORD, state=tk.DISABLED, bg="#f8f9fa", fg="#22223b", font=("Arial", 12))
        self.feedback_text.pack(padx=8, pady=4, fill=tk.BOTH, expand=True)

        # Status bar
        self.status_label = tk.Label(root, text="Ready", bg="#d8f5e7", fg="#22223b", anchor="w", font=("Arial", 11, "bold"))
        self.status_label.pack(fill=tk.X, pady=4, padx=2)

        # Placeholder for background listener
        self.stop_listening = None
        self.audio_data = None

    def _prevent_same_lang(self, *_):
        if self.from_lang_var.get() == self.to_lang_var.get():
            messagebox.showwarning("Language Selection", "Please select different languages to translate from and to.")
            # Try to auto-correct
            langs = [l for l in self.from_lang_var.master.children.values() if isinstance(l, tk.OptionMenu)]
            if self.to_lang_var.get() == self.from_lang_var.get():
                # Pick next language in list
                idx = langs[0]['menu'].index(self.from_lang_var.get())
                new_idx = (idx + 1) % len(langs[0]['menu'].entrycget(0, "label"))
                self.to_lang_var.set(langs[0]['menu'].entrycget(new_idx, "label"))

    def _auto_scroll(self, widget):
        widget.see(tk.END)

    def clear_text(self):
        self.transcript_text.delete(1.0, tk.END)
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.config(state=tk.DISABLED)
        self.status_label.config(text="Ready", bg="#d8f5e7")

    def start_recording(self):
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.recording_start_time = datetime.datetime.now()
        self._update_timer_running = True
        self._update_timer()
        self.status_label.config(text="Recording... (press Stop to finish)", bg="#ffe066")
        try:
            self.stop_listening = self.recognizer.listen_in_background(
                self.mic,
                self._callback,
                phrase_time_limit=None  # No auto-stop, user must press Stop
            )
        except Exception as e:
            messagebox.showerror("Microphone Error", f"Microphone error: {e}")
            self.reset_buttons()
            self.status_label.config(text="Error: Microphone not available", bg="#ffb4a2")

    def stop_recording(self):
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
        self.stop_button.config(state=tk.DISABLED)
        self._update_timer_running = False
        self.status_label.config(text="Stopped recording. Processing...", bg="#b5c1d8")

    def _update_timer(self):
        if hasattr(self, '_update_timer_running') and self._update_timer_running:
            elapsed = (datetime.datetime.now() - self.recording_start_time).total_seconds()
            self.status_label.config(text=f"Recording... {int(elapsed)}s (press Stop to finish)", bg="#ffe066")
            self.root.after(1000, self._update_timer)

    def _callback(self, recognizer, audio):
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
        self.audio_data = audio
        self.root.after(0, self.process_audio)

    def process_audio(self):
        # Recognize speech
        try:
            transcript = self.recognizer.recognize_google(self.audio_data)
        except Exception:
            transcript = "[Could not recognize speech. Please try again.]"
            self.status_label.config(text="Could not recognize speech.", bg="#ffb4a2")
        self.transcript_text.delete(1.0, tk.END)
        self.transcript_text.insert(tk.END, transcript)
        self._auto_scroll(self.transcript_text)
        self._translate(transcript)

    def manual_translate(self):
        transcript = self.transcript_text.get(1.0, tk.END).strip()
        if not transcript:
            messagebox.showinfo("Input Needed", "Please type or record something to translate.")
            return
        self._translate(transcript)

    def _translate(self, transcript):
        from_lang = self.from_lang_var.get()
        to_lang = self.to_lang_var.get()
        if from_lang == to_lang:
            messagebox.showwarning("Language Selection", "Please select different languages to translate from and to.")
            self.status_label.config(text="Error: Same language selected.", bg="#ffb4a2")
            return
        prompt = f"Translate from {from_lang} to {to_lang}: {transcript}"
        self.status_label.config(text="Translating...", bg="#b5c1d8")
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, "Translating, please wait...\n")
        self.feedback_text.config(state=tk.DISABLED)
        self._auto_scroll(self.feedback_text)
        # Run translation in a thread to keep UI responsive
        threading.Thread(target=self._do_translation, args=(prompt, transcript), daemon=True).start()

    def _do_translation(self, prompt, transcript):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3.2", "prompt": prompt, "stream": False}
            )
            response.raise_for_status()
            ai_feedback = response.json().get("response", "")
            self.root.after(0, lambda: self._show_feedback(ai_feedback, transcript, prompt))
        except requests.exceptions.ConnectionError:
            self.root.after(0, lambda: self._show_feedback("[Ollama is not running. Please start `ollama serve` and try again.]", transcript, prompt, error=True))
        except Exception as e:
            self.root.after(0, lambda: self._show_feedback(f"[Error from Ollama API: {e}]", transcript, prompt, error=True))

    def _show_feedback(self, ai_feedback, transcript, prompt, error=False):
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, ai_feedback)
        self.feedback_text.config(state=tk.DISABLED)
        self._auto_scroll(self.feedback_text)
        if error:
            self.status_label.config(text="Error during translation.", bg="#ffb4a2")
        else:
            self.status_label.config(text="Done.", bg="#cddafd")
        # Logging
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = os.path.join("logs", f"{timestamp}.txt")
        with open(log_filename, "w") as f:
            f.write("Transcript:\n")
            f.write(transcript + "\n\n")
            f.write("Prompt:\n")
            f.write(prompt + "\n\n")
            f.write("AI Feedback:\n")
            f.write(ai_feedback + "\n")
        self.reset_buttons()

    def reset_buttons(self):
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Launch the application
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()

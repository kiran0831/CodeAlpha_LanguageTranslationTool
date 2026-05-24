# ============================================================
#   Language Translation Tool
#   CodeAlpha AI Internship — Task 1
#   Built with Python, Tkinter, and Google Translate API
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
import subprocess

# Auto-install dependencies if missing
def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Installing deep-translator...")
    install("deep-translator")
    from deep_translator import GoogleTranslator

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# ── Language Map ─────────────────────────────────────────────
LANGUAGES = {
    "Auto Detect":          "auto",
    "Afrikaans":            "af",
    "Arabic":               "ar",
    "Bengali":              "bn",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)":"zh-TW",
    "Czech":                "cs",
    "Danish":               "da",
    "Dutch":                "nl",
    "English":              "en",
    "Finnish":              "fi",
    "French":               "fr",
    "German":               "de",
    "Greek":                "el",
    "Gujarati":             "gu",
    "Hebrew":               "iw",
    "Hindi":                "hi",
    "Hungarian":            "hu",
    "Indonesian":           "id",
    "Italian":              "it",
    "Japanese":             "ja",
    "Kannada":              "kn",
    "Korean":               "ko",
    "Malay":                "ms",
    "Malayalam":            "ml",
    "Marathi":              "mr",
    "Norwegian":            "no",
    "Persian":              "fa",
    "Polish":               "pl",
    "Portuguese":           "pt",
    "Punjabi":              "pa",
    "Romanian":             "ro",
    "Russian":              "ru",
    "Spanish":              "es",
    "Swahili":              "sw",
    "Swedish":              "sv",
    "Tamil":                "ta",
    "Telugu":               "te",
    "Thai":                 "th",
    "Turkish":              "tr",
    "Ukrainian":            "uk",
    "Urdu":                 "ur",
    "Vietnamese":           "vi",
}

# ── Colour Palette ────────────────────────────────────────────
BG_DARK   = "#1a1a2e"
BG_CARD   = "#16213e"
BG_ACCENT = "#0f3460"
RED       = "#e94560"
TEAL      = "#00d4aa"
TEXT      = "#e2e2e2"
MUTED     = "#a8a8b3"


# ─────────────────────────────────────────────────────────────
class TranslationApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🌐 Language Translation Tool  |  CodeAlpha")
        self.root.geometry("950x680")
        self.root.minsize(700, 520)
        self.root.configure(bg=BG_DARK)

        self._setup_styles()
        self._build_header()
        self._build_lang_row()
        self._build_text_area()
        self._build_buttons()
        self._build_statusbar()

    # ── Styles ────────────────────────────────────────────────
    def _setup_styles(self):
        s = ttk.Style()
        s.theme_use("clam")

        s.configure("App.TFrame",        background=BG_DARK)
        s.configure("Card.TFrame",       background=BG_CARD)

        s.configure("H1.TLabel",         background=BG_DARK, foreground=RED,
                                          font=("Helvetica", 22, "bold"))
        s.configure("Sub.TLabel",        background=BG_DARK, foreground=MUTED,
                                          font=("Helvetica", 10))
        s.configure("Caption.TLabel",    background=BG_DARK, foreground=TEXT,
                                          font=("Helvetica", 11, "bold"))

        s.configure("TCombobox",
                    fieldbackground=BG_ACCENT, background=BG_ACCENT,
                    foreground=TEXT, selectbackground=RED,
                    font=("Helvetica", 11))

        s.configure("Primary.TButton",
                    background=RED, foreground="white",
                    font=("Helvetica", 12, "bold"), padding=(28, 10))
        s.map("Primary.TButton", background=[("active", "#c73652")])

        s.configure("Ghost.TButton",
                    background=BG_ACCENT, foreground=TEXT,
                    font=("Helvetica", 10), padding=(12, 7))
        s.map("Ghost.TButton", background=[("active", "#1a4a7a")])

    # ── Header ────────────────────────────────────────────────
    def _build_header(self):
        f = ttk.Frame(self.root, style="App.TFrame")
        f.pack(fill="x", padx=30, pady=(20, 4))

        ttk.Label(f, text="🌐  Language Translation Tool",
                  style="H1.TLabel").pack(side="left")
        ttk.Label(f, text="Google Translate  •  CodeAlpha AI Internship",
                  style="Sub.TLabel").pack(side="right", pady=(10, 0))

        tk.Frame(self.root, bg=RED, height=2).pack(fill="x", padx=30, pady=4)

    # ── Language Selection ─────────────────────────────────────
    def _build_lang_row(self):
        f = ttk.Frame(self.root, style="App.TFrame")
        f.pack(fill="x", padx=30, pady=8)

        # Source
        sf = ttk.Frame(f, style="App.TFrame")
        sf.pack(side="left", expand=True, fill="x")
        ttk.Label(sf, text="Source Language", style="Caption.TLabel").pack(anchor="w")
        self.src_var = tk.StringVar(value="Auto Detect")
        ttk.Combobox(sf, textvariable=self.src_var,
                     values=list(LANGUAGES.keys()),
                     state="readonly", font=("Helvetica", 11)
                     ).pack(fill="x", pady=(4, 0))

        # Swap
        mf = ttk.Frame(f, style="App.TFrame")
        mf.pack(side="left", padx=18, pady=(18, 0))
        tk.Button(mf, text="⇄", bg=BG_ACCENT, fg=RED,
                  font=("Helvetica", 17, "bold"), bd=0,
                  cursor="hand2", relief="flat",
                  activebackground="#1a4a7a", activeforeground=RED,
                  command=self._swap_langs).pack()

        # Target
        tf = ttk.Frame(f, style="App.TFrame")
        tf.pack(side="left", expand=True, fill="x")
        ttk.Label(tf, text="Target Language", style="Caption.TLabel").pack(anchor="w")
        self.tgt_var = tk.StringVar(value="Hindi")
        ttk.Combobox(tf, textvariable=self.tgt_var,
                     values=[l for l in LANGUAGES if l != "Auto Detect"],
                     state="readonly", font=("Helvetica", 11)
                     ).pack(fill="x", pady=(4, 0))

    # ── Text Areas ─────────────────────────────────────────────
    def _build_text_area(self):
        f = ttk.Frame(self.root, style="App.TFrame")
        f.pack(fill="both", expand=True, padx=30, pady=6)
        f.columnconfigure(0, weight=1)
        f.columnconfigure(1, weight=1)
        f.rowconfigure(1, weight=1)

        # Labels
        ttk.Label(f, text="✏️  Input Text",
                  style="Caption.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 4))
        ttk.Label(f, text="📄  Translated Text",
                  style="Caption.TLabel").grid(row=0, column=1, sticky="w",
                                                padx=(14, 0), pady=(0, 4))

        # Input box
        self.input_box = tk.Text(
            f, font=("Helvetica", 13),
            bg=BG_CARD, fg=TEXT, insertbackground="white",
            relief="flat", wrap="word", padx=12, pady=12,
            highlightthickness=1,
            highlightbackground=BG_ACCENT, highlightcolor=RED
        )
        self.input_box.grid(row=1, column=0, sticky="nsew")

        in_sb = ttk.Scrollbar(f, command=self.input_box.yview)
        in_sb.grid(row=1, column=0, sticky="nse")
        self.input_box.configure(yscrollcommand=in_sb.set)

        # Output box
        self.output_box = tk.Text(
            f, font=("Helvetica", 13),
            bg=BG_CARD, fg=TEAL,
            relief="flat", wrap="word", padx=12, pady=12,
            state="disabled",
            highlightthickness=1,
            highlightbackground=BG_ACCENT, highlightcolor=RED
        )
        self.output_box.grid(row=1, column=1, sticky="nsew", padx=(14, 0))

        out_sb = ttk.Scrollbar(f, command=self.output_box.yview)
        out_sb.grid(row=1, column=1, sticky="nse", padx=(14, 0))
        self.output_box.configure(yscrollcommand=out_sb.set)

    # ── Buttons ────────────────────────────────────────────────
    def _build_buttons(self):
        f = ttk.Frame(self.root, style="App.TFrame")
        f.pack(fill="x", padx=30, pady=(6, 16))

        ttk.Button(f, text="🔁  Translate",
                   style="Primary.TButton",
                   command=self._translate).pack(side="left")

        ttk.Button(f, text="🗑  Clear",
                   style="Ghost.TButton",
                   command=self._clear).pack(side="left", padx=(10, 0))

        ttk.Button(f, text="📋  Copy",
                   style="Ghost.TButton",
                   command=self._copy).pack(side="left", padx=(10, 0))

        if TTS_AVAILABLE:
            ttk.Button(f, text="🔊  Speak",
                       style="Ghost.TButton",
                       command=self._speak).pack(side="left", padx=(10, 0))

    # ── Status Bar ────────────────────────────────────────────
    def _build_statusbar(self):
        self.status = tk.StringVar(value="  Ready — Enter text and click Translate")
        tk.Label(self.root, textvariable=self.status,
                 bg=BG_ACCENT, fg=MUTED,
                 font=("Helvetica", 9), anchor="w",
                 padx=12, pady=5
                 ).pack(fill="x", side="bottom")

    # ── Actions ───────────────────────────────────────────────
    def _translate(self):
        text = self.input_box.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Empty Input", "Please enter some text to translate.")
            return

        src = LANGUAGES[self.src_var.get()]
        tgt = LANGUAGES[self.tgt_var.get()]

        if src == tgt:
            messagebox.showinfo("Same Language", "Source and target languages are the same.")
            return

        self.status.set("  ⏳ Translating…")
        self.root.update_idletasks()

        def worker():
            try:
                result = GoogleTranslator(source=src, target=tgt).translate(text)
                self.output_box.configure(state="normal")
                self.output_box.delete("1.0", "end")
                self.output_box.insert("1.0", result)
                self.output_box.configure(state="disabled")
                self.status.set(
                    f"  ✅  Translated: {self.src_var.get()} → {self.tgt_var.get()}"
                    f"  |  {len(text)} chars input"
                )
            except Exception as exc:
                messagebox.showerror("Translation Error", str(exc))
                self.status.set("  ❌  Translation failed. Check your internet connection.")

        threading.Thread(target=worker, daemon=True).start()

    def _swap_langs(self):
        if self.src_var.get() == "Auto Detect":
            messagebox.showinfo("Swap", "Cannot swap when source is 'Auto Detect'.")
            return
        src, tgt = self.src_var.get(), self.tgt_var.get()
        self.src_var.set(tgt)
        self.tgt_var.set(src)

        in_t  = self.input_box.get("1.0", "end-1c")
        out_t = self.output_box.get("1.0", "end-1c")

        self.input_box.delete("1.0", "end")
        self.input_box.insert("1.0", out_t)

        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", in_t)
        self.output_box.configure(state="disabled")
        self.status.set("  ⇄  Languages swapped")

    def _clear(self):
        self.input_box.delete("1.0", "end")
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.configure(state="disabled")
        self.status.set("  Cleared — Ready for new translation")

    def _copy(self):
        text = self.output_box.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showinfo("Nothing to Copy", "Translate something first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status.set("  📋  Translation copied to clipboard!")

    def _speak(self):
        text = self.output_box.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showinfo("Nothing to Speak", "Translate something first.")
            return

        def worker():
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception as exc:
                messagebox.showerror("TTS Error", str(exc))

        threading.Thread(target=worker, daemon=True).start()
        self.status.set("  🔊  Speaking translation…")


# ── Entry Point ───────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()

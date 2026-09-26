import math
import random
import tkinter as tk
from tkinter import messagebox

PRESETS = {
    "Cyberpunk": {
        "bg": "#0d0f18",
        "input_bg": "#16192b",
        "input_border": "#00f0ff",
        "btn_bg": "#ff0055",
        "btn_border": "#ffffff",
        "particle": "#00f0ff"
    },
    "Emerald": {
        "bg": "#061a14",
        "input_bg": "#0b2e23",
        "input_border": "#10b981",
        "btn_bg": "#059669",
        "btn_border": "#a7f3d0",
        "particle": "#34d399",
    },
    "Midnight": {
        "bg": "#0f081d",
        "input_bg": "#1c0f35",
        "input_border": "#a855f7",
        "btn_bg": "#7e22ce",
        "btn_border": "#e9d5ff",
        "particle": "#c084fc",
    },
    "Sunset": {
        "bg": "#1a0c1a",
        "input_bg": "#2d152b",
        "input_border": "#f43f5e",
        "btn_bg": "#fb923c",
        "btm_border": "#fef08a",
        "particle": "#f43f5e",
    },
    "Mono": {
        "bg": "#121212",
        "input_bg": "#1e1e1e",
        "input_border": "#444444",
        "btn_bg": "#2d2d2d",
        "btn_border": "#888888",
        "particle": "#666666",
    },
}

OUTCOMES = [
    {
        "text": "DIVINE INTERVENTION SAYS YES",
        "weight": 0.5,
        "type": "divine",
        "pct": "0.5%",
    
    },
    {
        "text": "1000% ABSOLUTELY!",
        "weight": 1.0,
        "type": "legendary",
        "pct": "1.0%",
    },
    {
        "text": "NAH BRO NOT IN A MILLION YEARS",
        "weight": 3.0,
        "type": "rare_no",
        "pct": "3.0%",
    },
    {"text": "HELL YEAH!", "weight": 6.0, "type": "rare_yes", "pct": "6.0%"},
    {"text": "ABSOLUTELY NOT", "weight": 6.0, "type": "rare_no", "pct": "6.0%"},
    {"text": "Of course", "weight": 6.0, "type": "rare_yes", "pct": "6.0%"},
    {"text": "YES", "weight": 20.0, "type": "yes", "pct": "20.0%"},
    {"text": "Yeah", "weight": 20.0, "type": "yes", "pct": "20.0%"},
    {"text": "Nope", "weight": 18.75, "type": "no", "pct": "18.75%"},
    {"text": "Nah", "weight": 18.75, "type": "no", "pct": "18.75%"},
]


class DecisionBotPython:
    def __init__(self, root):
        self.root = root
        self.root.title("OPSEC Decision Bot")
        self.root.geometry("800x650")

        self.current_theme = PRESETS["Cyberpunk"]
        self.root.configure(bg=self.current_theme["bg"])

        self.bg_mode = "constellation"
        self.opsec_active = False
        self.forced_outcome = None
        self.current_outcome = None
        self.particles = [
            {
                "x": random.randint(0, 800),
                "y": random.randint(0,650),
                "vx": random.uniform(-1, 1),
                "vy": random.uniform(-1, 1),
            }
            for _ in range(40)
        ]
        self.binary_drops = [random.randint(-30, 0) for _ in range(40)]
        self.gold_particles = []
        self.flash_opacity = 0
        self.color_shift = 0

        self.setup_ui()
        self.setup_keybinds()
        self.animate()

    def setup_ui(self):
        self.canvas = tk.Canvas(
            self.root, bg=self.current_theme["bg"], highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.lbl_title = tk.Label(
            self.root,
            text="DECISION BOT",
            fg="#ffffff",
            bg=self.current_theme["bg"],
            font=("Consolas", 18, "bold"),
        )
        self.lbl_title.place(relx=0.5, rely=0.08, anchor="center")

        self.entry_q = tk.Entry(
            self.root,
            font=("Helvetica", 14),
            bg=self.current_theme["input_bg"],
            fg="#ffffff",
            insertbackground="#ffffff",
            bd=0,
            justify="center",
        )
        self.entry_q.insert(0, "Should I follow my dreams?")
        self.entry_q.place(
            relx=0.5, rely=0.20, width=420, height=45, anchor="center"
        )

        self.lbl_pct = tk.Label(
            self.root,
            text="",
            fg="#00f0ff",
            bg=self.current_theme["bg"],
            font=("Consolas", 11, "bold"),
        )
        self.lbl_pct.place(relx=0.5, rely=0.38, anchor="center")

        self.btn_send = tk.Button(
            self.root,
            text="SEND",
            command=self.on_roll,
            bg=self.current_theme["btn_bg"],
            fg="#ffffff",
            activebackground=self.current_theme["btn_border"],
            activeforeground="#000000",
            bd=0,
            font=("Helvetica", 12, "bold"),
            cursor="hand2",
        )
        self.btn_send.place(
            relx=0.5, rely=0.62, width=220, height=45, anchor="center"
        )

        self.preset_frame = tk.Frame(self.root, bg=self.current_theme["bg"])
        self.preset_frame.place(relx=0.5, rely=0.92, anchor="center")

        for key in PRESETS:
            btn = tk.Button(
                self.preset_frame,
                text=key,
                font=("Helvetica", 8, "bold"),
                bg=PRESETS[key]["btn_bg"],
                fg="#ffffff",
                bd=0,
                command=lambda k=key: self.apply_preset(k),
            )
            btn.pack(side="left", padx=3)

    

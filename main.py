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

    def setup_keybinds(self):
        self.root.bind("<Shift-Alt-A>", self.enable_opsec)
        self.root.bind("<Shift-Alt-a>", self.enable_opsec)
        self.root.bind("<Shift-Alt-D>", self.disable_opsec)
        self.root.bind("<Shift-Alt-d>", self.disable_opsec)

    def apply_preset(self, key):
        self.current_theme = PRESETS[key]
        self.root.configure(bg=self.current_theme["bg"])
        self.canvas.configure(bg=self.current_theme["bg"])
        self.lbl_title.configure(bg=self.current_theme["bg"])
        self.lbl_pct.configure(bg=self.current_theme["bg"])
        self.preset_frame.configure(bg=self.current_theme["bg"])
        self.btn_send.confiure(
            bg=self.current_theme["btn_bg"],
            activebackround=self.current_theme["btn_border"]
        )
        self.entry_q.configure(bg=self.current_theme["input_bg"])

    def enable_opsec(self, event=None):
        self.opsec_active = True
        self.bg_mode = "binary"
        self.forced_outcome = OUTCOMES[0]
        self.lbl_title.configure(
            text="[OPSEC MODE ACTIVATED]", fg="#00ff66"
        )
        messagebox.showinfo(
            "OPSEC",
            "Sudo apt install opsec mode activated!\nNext roll forced to DIVINE INTERVENTION.",
        )

    def disable_opsec(self, event=None):
        self.opsec_active = False
        self.bg_mode = "constellation"
        self.forced_outcome = None
        self.lbl_title.configure(text="DECISION BOT", fg="#ffffff")

    def draw_flat_cylinder(
        self,
        x,
        y,
        w,
        h,
        fill_color,
        border_color,
        text="",
        font=("Helvetica", 12, "bold"),
        text_color="#ffffff",
        tag="cyl",
    ):
        self.canvas.delete(tag)
        r = h / 2
        self.canvas.create_oval(
            x,
            y,
            x + 2 * r,
            y + h,
            fill=fill_color,
            outline=border_color,
            width=2,
            tags=tag,
        )
        self.canvas.create_oval(
            x + w - 2 * r,
            y,
            x + w,
            y + h,
            fill=fill_color,
            outline=border_color,
            width=2,
            tags=tag,
        )
        self.canvas.create_rectangle(
            x + r,
            y,
            x + w - r,
            y + h,
            fill=fill_color,
            outline="",
            tags=tag,
        )
        self.canvas.create_line(
            x + r, y, x + w - r, y, fill=border_color, width=2, tags=tag
        )
        self.canvas.create_line(
            x + r, y + h, x + w - r, y + h, fill=border_color, width=2, tags=tag
        )

        if text:
            self.canvas.create_text(
                x + w / 2,
                y + h / 2,
                text=text,
                fill=text_color,
                font=font,
                tags=tag,
            )

    def trigger_divine_fx(self):
        self.flash_opacity = 1.0
        self.gold_particles = []
        for _ in range(75):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 9)
            self.gold_particles.append(
                {
                    "x": 400,
                    "y": 290,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "alpha": 1.0,
                }
            )

    def on_roll(self):
        if (
            self.current_outcome
            and self.current_outcome["weight"] <= 1.0
            and not self.opsec_active
        ):
            skip = messagebox.askyesno(
                "Rare Outcome",
                "Are you sure you wanna skip this and not screenshot it? Thats pretty rare bro!"
            )
            if not skip:
                return

        if self.forced_outcome:
            selected = self.forced_outcome
        else:
            weights = [o["weight"] for o in OUTCOMES]
            selected = random.choices(OUTCOMES, weights=weights, k=1[0])

        self.current_outcome = selected
        self.lbl_pct.configure(
            text=f"CHANCE: {selected['pct']}",
            fg=(
                "#ffd700"
                if selected["type"] == "divine"
                else (
                    "#10b981"
                    if "yes" in selected["type"] or selected["type"] == "legendary"
                    else "#ef4444"
                )
            ),
        )

        if selected["type"] == "divine":
            self.trigger_divine_fx()

    def animate(self):
        self.canvas.delete("bg")
        self.canvas.delete("divine_fx")
        w, h = 800, 650

        if self.bg_mode == "constellation":
            for i, p in enumerate(self.particles):
                p["x"] = (p["x"] + p["vx"]) % w
                p["y"] = (p["y"] + p["vy"]) % h
                self.canvas.create_oval(
                    p["x"] - 2,
                    p["y"] - 2,
                    p["x"] + 2,
                    p["y"] + 2,
                    fill=self.current_theme["particle"],
                    outline="",
                    tags="bg",
                )
                for p2 in self.particles[i + 1 :]:
                    dist = math.hypot(p["x"] - p2["x"], p["y"] - p2["y"])
                    if dist < 110:
                        self.canvas.create_line(
                            p["x"],
                            p["y"],
                            p2["x"],
                            p2["y"],
                            fill=self.current_theme["particle"],
                            width=1,
                            tags="bg",
                        )
        elif self.bg_mode == "binary":
            for i in range(40):
                x = i * 20
                self.binary_drops[i] += 1
                if self.binary_drops[i] * 20 > h:
                    self.binary_drops[i] = 0
                char = random.choice(["0", "1"])
                self.canvas.create_text(
                    x,
                    self.binary_drops[i] * 20,
                    text=char,
                    fill="#00ff66",
                    font=("Consolas", 12),
                    tags="bg",
                )
        box_fill = self.current_theme["input_bg"]
        box_border = self.current_theme["input_border"]
        text_color = "#ffffff"
        font = ("Helvetica", 12, "bold")

        if self.current_outcome:
            otype = self.current_outcome["type"]
            if otype == "divine":
                self.color_shift = (self.color_shift + 0.05) % (2 * math.pi)
                val = int(200 + 55 * math.sin(self.color_shift))
                box_fill = f"{val:02x}a000"
                box_border = "#ffd700"
                font = ("Georgia", 11, "bold")
                text_color = "#fff8dc"

                # The stupid halo thingy
                self.canvas.create_oval(
                    320,
                    225,
                    480,
                    245,
                    outline="#ffd700",
                    width=4,
                    tags="divine_fx",
                )
            elif otype == "legendary" or "yes" in otype:
                text_color = "#10b981"
                box_border = "#10b981"
            elif "no" in otype:
                text_color = "#ef4444"
                box_border = "#ef4444"

        display_text = (
            self.current_outcome["text"]
            if self.current_outcome
            else "ASK A QUESTION & ROLL"
        )
        self.draw_flat_cylinder(
            180,
            260,
            440,
            60,
            box_fill,
            box_border,
            text=display_text,
            font=font,
            text_color=text_color,
            tag="answer_box",
        )

        for p in self.gold_particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["alpha"] -= 0.02
            if p["alpha"] > 0:
                self.canvas.create_oval(
                    p["x"] - 3,
                    p["y"] - 3,
                    p["x"] + 3,
                    p["y"] + 3,
                    fill="#ffd700",
                    outline="",
                    tags="divine_fx",
                )
        self.gold_particles = [p for p in self.gold_particles if p["alpha"] > 0]

        if self.flash_opacity > 0:
            self.canvas.create_rectangle(
                0, 0, w, h, fill="#fffbea", outline="", tags="divine_fx"
            )
            self.flash_opacity -= 0.1

        self.root.after(30, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = DecisionBotPython(root)
    root.mainloop()

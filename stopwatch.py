import customtkinter as ctk
import tkinter as tk
import time
import math
import pygame
import os

LAP_SOUND = "lap.mp3"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class UltraStopwatch(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Ultra Stopwatch")
        self.geometry("420x650")
        self.resizable(False, False)

        pygame.mixer.init()

        self.running = False
        self.start_time = 0
        self.elapsed = 0
        self.laps = []

        self.create_background()
        self.create_glass_panel()

    # ---------- ГРАДІЄНТ ----------
    def create_background(self):
        self.canvas_bg = tk.Canvas(self, width=420, height=650, highlightthickness=0)
        self.canvas_bg.place(x=0, y=0)
        self.draw_gradient("#667eea", "#764ba2")

    def draw_gradient(self, c1, c2):
        for i in range(650):
            r1, g1, b1 = self.winfo_rgb(c1)
            r2, g2, b2 = self.winfo_rgb(c2)

            r = int(r1 + (r2 - r1) * i / 650) >> 8
            g = int(g1 + (g2 - g1) * i / 650) >> 8
            b = int(b1 + (b2 - b1) * i / 650) >> 8

            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas_bg.create_line(0, i, 420, i, fill=color)

    # ---------- GLASS PANEL ----------
    def create_glass_panel(self):
        self.glass = ctk.CTkFrame(self,
                                  width=350,
                                  height=580,
                                  corner_radius=30,
                                  fg_color=("#ffffff", "#1a1a1a"),
                                  bg_color="transparent")
        self.glass.place(relx=0.5, rely=0.5, anchor="center")

        self.create_ui()

    # ---------- UI ----------
    def create_ui(self):

        title = ctk.CTkLabel(self.glass,
                             text="STOPWATCH",
                             font=("Segoe UI", 24, "bold"))
        title.pack(pady=15)

        # КРУГЛИЙ ПРОГРЕС
        self.canvas = tk.Canvas(self.glass, width=250, height=250,
                                bg=self.glass.cget("fg_color")[1],
                                highlightthickness=0)
        self.canvas.pack(pady=20)

        self.arc = self.canvas.create_arc(20, 20, 230, 230,
                                          start=90,
                                          extent=0,
                                          width=15,
                                          style="arc",
                                          outline="#4CAF50")

        self.time_text = self.canvas.create_text(125, 125,
                                                 text="00:00.00",
                                                 fill="white",
                                                 font=("Segoe UI", 26, "bold"))

        # КНОПКИ
        btn_frame = ctk.CTkFrame(self.glass, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(btn_frame, text="Старт",
                      command=self.start).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Стоп",
                      command=self.stop).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Скинути",
                      command=self.reset).pack(side="left", padx=5)

        ctk.CTkButton(self.glass, text="Коло (Lap)",
                      command=self.add_lap).pack(pady=10)

        # СПИСОК КІЛ
        self.lap_box = ctk.CTkTextbox(self.glass, width=300, height=150)
        self.lap_box.pack(pady=10)
        self.lap_box.configure(state="disabled")

    # ---------- ФОРМАТ ЧАСУ ----------
    def format_time(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 100)
        return f"{mins:02}:{secs:02}.{millis:02}"

    # ---------- ОНОВЛЕННЯ ----------
    def update_time(self):
        if self.running:
            self.elapsed = time.time() - self.start_time
            formatted = self.format_time(self.elapsed)

            self.canvas.itemconfig(self.time_text, text=formatted)

            # Круг обертається кожну секунду
            progress = (self.elapsed % 1)
            extent = -360 * progress
            self.canvas.itemconfig(self.arc, extent=extent)

            self.after(10, self.update_time)

    # ---------- КЕРУВАННЯ ----------
    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed
            self.running = True
            self.update_time()

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.elapsed = 0
        self.canvas.itemconfig(self.time_text, text="00:00.00")
        self.canvas.itemconfig(self.arc, extent=0)
        self.laps.clear()
        self.lap_box.configure(state="normal")
        self.lap_box.delete("1.0", "end")
        self.lap_box.configure(state="disabled")

    def add_lap(self):
        if self.running:
            lap_time = self.format_time(self.elapsed)
            self.laps.append(lap_time)

            self.lap_box.configure(state="normal")
            self.lap_box.insert("end", f"Коло {len(self.laps)} — {lap_time}\n")
            self.lap_box.configure(state="disabled")

            if os.path.exists(LAP_SOUND):
                pygame.mixer.music.load(LAP_SOUND)
                pygame.mixer.music.play()

if __name__ == "__main__":
    app = UltraStopwatch()
    app.mainloop()
import tkinter as tk
from tkinter import messagebox, font
import math


class AutoBulbSystemModern:
    def __init__(self, master):
        self.master = master
        self.master.title("💡 Smart Bulb Control System")
        self.master.configure(bg="#1a1a2e")  # Deep dark blue background
        
        self.master.resizable(True, True)

        # Bulb state: False = OFF, True = ON
        self.bulb_on = False
        self.motion_detected = False

        # Custom fonts
        self.title_font = font.Font(family="Segoe UI", size=18, weight="bold")
        self.subtitle_font = font.Font(family="Segoe UI", size=12)
        self.button_font = font.Font(family="Segoe UI", size=11, weight="bold")
        self.status_font = font.Font(family="Segoe UI", size=14, weight="bold")
        self.info_font = font.Font(family="Segoe UI", size=10)

        # Create main container with gradient effect
        self.create_gradient_background()

        # Title with shadow effect
        self.title_frame = tk.Frame(
            master,
            bg="#16213e",
            highlightbackground="#0f3460",
            highlightthickness=2,
        )
        self.title_frame.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(
            self.title_frame,
            text="💡 SMART BULB CONTROL",
            font=self.title_font,
            fg="#e94560",
            bg="#16213e",
        ).pack(pady=10)

        tk.Label(
            self.title_frame,
            text="Simple Reflex Agent Based System",
            font=self.subtitle_font,
            fg="#888888",
            bg="#16213e",
        ).pack(pady=(0, 10))

        # Bulb display frame with 3D effect
        self.bulb_frame = tk.Frame(
            master,
            bg="#0f3460",
            bd=0,
            highlightbackground="#e94560",
            highlightthickness=2,
        )
        self.bulb_frame.pack(pady=30, padx=40, fill="both")

        # Canvas for bulb visualization
        self.canvas = tk.Canvas(
            self.bulb_frame,
            width=200,
            height=200,
            bg="#0f3460",
            highlightthickness=0,
        )
        self.canvas.pack(pady=20)

        # Draw bulb base
        self.draw_bulb_base()

        # Draw bulb (initially OFF)
        self.bulb_body = self.draw_bulb_off()

        # Bulb status label with modern styling
        self.status_frame = tk.Frame(self.bulb_frame, bg="#0f3460")
        self.status_frame.pack(pady=(0, 20))

        self.bulb_label = tk.Label(
            self.status_frame,
            text="⚫ BULB OFF",
            font=self.status_font,
            bg="#0f3460",
            fg="#888888",
            width=15,
        )
        self.bulb_label.pack()

        # Motion status indicator
        self.motion_indicator = tk.Label(
            self.bulb_frame,
            text="● NO MOTION",
            font=self.info_font,
            bg="#0f3460",
            fg="#888888",
        )
        self.motion_indicator.pack(pady=(0, 15))

        # Button frame with modern layout
        self.button_frame = tk.Frame(master, bg="#1a1a2e")
        self.button_frame.pack(pady=20, padx=40, fill="x")

        # Create styled buttons
        self.create_buttons()

        # Info panel
        self.create_info_panel()

        # Bind hover effects
        self.bind_hover_effects()

    def create_gradient_background(self):
        """Create a subtle gradient effect"""
        self.canvas_bg = tk.Canvas(self.master, width=500, height=600, highlightthickness=0)
        self.canvas_bg.place(x=0, y=0)

        # Create gradient lines
        for i in range(600):
            color = f'#{int(26 - i*0.02):02x}{int(26 - i*0.02):02x}{int(46 - i*0.03):02x}'
            self.canvas_bg.create_line(0, i, 500, i, fill=color, width=1)

        # Lower all items so gradient is behind other widgets
        for item in self.canvas_bg.find_all():
            self.canvas_bg.lower(item)

    def draw_bulb_base(self):
        """Draw the bulb base/socket"""
        self.canvas.create_rectangle(85, 150, 115, 170, fill="#333333", outline="#444444", width=2)
        self.canvas.create_oval(80, 165, 120, 175, fill="#555555", outline="#666666", width=2)

    def draw_bulb_off(self):
        """Draw bulb in OFF state"""
        return self.canvas.create_oval(50, 30, 150, 140, fill="#2a2a2a", outline="#444444", width=3)

    def draw_bulb_on(self):
        """Draw bulb in ON state with glow effect"""
        for i in range(5, 0, -1):
            alpha = int(255 - i * 40)
            color = f'#FFFF{alpha:02x}'
            self.canvas.create_oval(50-i, 30-i, 150+i, 140+i, fill="", outline=color, width=i)

        return self.canvas.create_oval(50, 30, 150, 140, fill="#ffff99", outline="#ffaa00", width=3)

    def create_buttons(self):
        """Create modern styled buttons"""
        button_configs = [
            ("🚶 PERSON ENTERS", self.person_enters, "#00b894", "#00cec9"),
            ("🚶 PERSON LEAVES", self.person_leaves, "#d63031", "#e17055"),
            ("🔄 RESET SYSTEM", self.reset_system, "#0984e3", "#74b9ff"),
        ]

        for i, (text, command, color, hover_color) in enumerate(button_configs):
            btn = tk.Button(
                self.button_frame,
                text=text,
                command=command,
                font=self.button_font,
                bg=color,
                fg="white",
                activebackground=hover_color,
                activeforeground="white",
                relief="flat",
                bd=0,
                width=20,
                height=2,
                cursor="hand2",
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
            btn.original_color = color
            btn.hover_color = hover_color

        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

    def create_info_panel(self):
        """Create information panel at bottom"""
        self.info_frame = tk.Frame(
            self.master, bg="#16213e", highlightbackground="#0f3460", highlightthickness=1
        )
        self.info_frame.pack(side="bottom", fill="x", padx=20, pady=20)

        info_text = "🤖 Simple Reflex Agent: Bulb turns ON when motion detected, OFF when no motion"
        tk.Label(
            self.info_frame,
            text=info_text,
            font=self.info_font,
            fg="#888888",
            bg="#16213e",
            wraplength=450,
            justify="center",
        ).pack(pady=10, padx=10)

    def bind_hover_effects(self):
        """Bind hover effects to buttons"""
        for child in self.button_frame.winfo_children():
            if isinstance(child, tk.Button):
                child.bind("<Enter>", lambda e, btn=child: self.on_enter(btn))
                child.bind("<Leave>", lambda e, btn=child: self.on_leave(btn))

    def on_enter(self, button):
        button.config(bg=button.hover_color, relief="sunken")

    def on_leave(self, button):
        button.config(bg=button.original_color, relief="flat")

    def update_bulb(self):
        self.canvas.delete("all")
        self.draw_bulb_base()

        if self.motion_detected:
            self.bulb_on = True
            self.draw_bulb_on()
            self.bulb_label.config(text="💡 BULB ON", fg="#ffff99", bg="#0f3460")
            self.motion_indicator.config(text="● MOTION DETECTED", fg="#00b894")
            self.animate_bulb()
        else:
            self.bulb_on = False
            self.draw_bulb_off()
            self.bulb_label.config(text="⚫ BULB OFF", fg="#888888", bg="#0f3460")
            self.motion_indicator.config(text="● NO MOTION", fg="#d63031")

    def animate_bulb(self):
        if self.motion_detected:
            current_color = self.canvas.itemcget(self.bulb_body, "fill")
            if current_color == "#ffff99":
                self.canvas.itemconfig(self.bulb_body, fill="#ffff66")
            else:
                self.canvas.itemconfig(self.bulb_body, fill="#ffff99")
            self.master.after(500, self.animate_bulb)

    def person_enters(self):
        self.motion_detected = True
        self.update_bulb()
        self.show_notification("✅ Person Entered!", "Bulb turned ON automatically", "#00b894")

    def person_leaves(self):
        self.motion_detected = False
        self.update_bulb()
        self.show_notification("👋 Person Left!", "Bulb turned OFF automatically", "#d63031")

    def reset_system(self):
        self.motion_detected = False
        self.update_bulb()
        self.show_notification("🔄 System Reset", "Bulb turned OFF", "#0984e3")

    def show_notification(self, title, message, color):
        notif_frame = tk.Frame(self.master, bg=color, bd=0)
        notif_frame.place(relx=0.5, rely=0.1, anchor="center")

        tk.Label(notif_frame, text=title, font=self.button_font, fg="white", bg=color).pack(
            padx=20, pady=(10, 5)
        )
        tk.Label(notif_frame, text=message, font=self.info_font, fg="white", bg=color).pack(
            padx=20, pady=(0, 10)
        )

        self.master.after(2000, notif_frame.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoBulbSystemModern(root)
    root.mainloop()
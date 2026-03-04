import tkinter as tk
from tkinter import ttk

from mission_state import MissionState
from reasoning_engine import ReasoningEngine


class MissionControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Autonomous Space Mission Survival Agent")
        self.geometry("1100x600")
        self.configure(bg="black")

        self.engine = ReasoningEngine()

        # Variables
        self.oxygen_var = tk.IntVar(value=80)
        self.power_var = tk.IntVar(value=70)
        self.food_var = tk.IntVar(value=75)
        self.fuel_var = tk.IntVar(value=65)
        self.hull_var = tk.IntVar(value=90)
        self.goal_text_var = tk.StringVar(value="Reach Mars")
        self.goal_days_var = tk.IntVar(value=20)

        self._build_styles()
        self._build_layout()
        self._update_outputs()

    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Mission.TFrame", background="black")
        style.configure(
            "Mission.TLabel",
            background="black",
            foreground="#00f5ff",
            font=("Consolas", 11),
        )
        # Use the proper ttk style name for horizontal progress bars.
        style.configure(
            "Mission.Horizontal.TProgressbar",
            troughcolor="#111",
            background="#00ff88",
        )

    def _build_layout(self):
        main = ttk.Frame(self, style="Mission.TFrame")
        main.pack(fill="both", expand=True, padx=16, pady=16)

        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.columnconfigure(2, weight=1)

        # Left: Inputs
        left = ttk.Frame(main, style="Mission.TFrame")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        ttk.Label(left, text="Input Systems", style="Mission.TLabel").pack(anchor="w")
        self._build_slider(left, "Oxygen", self.oxygen_var)
        self._build_slider(left, "Power", self.power_var)
        self._build_slider(left, "Food", self.food_var)
        self._build_slider(left, "Fuel", self.fuel_var)
        self._build_slider(left, "Hull Integrity", self.hull_var)

        ttk.Label(left, text="Mission Goal", style="Mission.TLabel").pack(
            anchor="w", pady=(12, 2)
        )
        goal_entry = tk.Entry(
            left,
            textvariable=self.goal_text_var,
            bg="#111",
            fg="#00f5ff",
            insertbackground="#00f5ff",
            relief="flat",
        )
        goal_entry.pack(fill="x", pady=(0, 8))

        ttk.Label(left, text="Goal Timeline (days)", style="Mission.TLabel").pack(
            anchor="w"
        )
        goal_days = tk.Spinbox(
            left,
            from_=1,
            to=200,
            textvariable=self.goal_days_var,
            bg="#111",
            fg="#00f5ff",
            insertbackground="#00f5ff",
            relief="flat",
            width=6,
            command=self._update_outputs,
        )
        goal_days.pack(anchor="w", pady=(0, 12))

        # Center: Gauges
        center = ttk.Frame(main, style="Mission.TFrame")
        center.grid(row=0, column=1, sticky="nsew", padx=12)

        ttk.Label(center, text="System Gauges", style="Mission.TLabel").pack(anchor="w")
        self._build_gauge(center, "Oxygen", self.oxygen_var)
        self._build_gauge(center, "Power", self.power_var)
        self._build_gauge(center, "Food", self.food_var)
        self._build_gauge(center, "Fuel", self.fuel_var)
        self._build_gauge(center, "Hull Integrity", self.hull_var)

        # Right: Output
        right = ttk.Frame(main, style="Mission.TFrame")
        right.grid(row=0, column=2, sticky="nsew", padx=(12, 0))

        ttk.Label(right, text="Strategic Output", style="Mission.TLabel").pack(anchor="w")
        self.output = tk.Text(
            right,
            height=26,
            bg="#050505",
            fg="#00ff88",
            insertbackground="#00ff88",
            relief="flat",
            wrap="word",
        )
        self.output.pack(fill="both", expand=True)
        self.output.configure(state="disabled")

        # Variable trace for real-time updates
        for var in [
            self.oxygen_var,
            self.power_var,
            self.food_var,
            self.fuel_var,
            self.hull_var,
            self.goal_text_var,
            self.goal_days_var,
        ]:
            var.trace_add("write", lambda *args: self._update_outputs())

    def _build_slider(self, parent, label, var):
        frame = ttk.Frame(parent, style="Mission.TFrame")
        frame.pack(fill="x", pady=6)

        ttk.Label(frame, text=f"{label}: {var.get()}%", style="Mission.TLabel").pack(
            anchor="w"
        )
        slider = tk.Scale(
            frame,
            from_=0,
            to=100,
            orient="horizontal",
            variable=var,
            bg="black",
            fg="#00f5ff",
            highlightthickness=0,
            troughcolor="#111",
            activebackground="#00f5ff",
        )
        slider.pack(fill="x")

        def update_label(*_):
            label_widget = frame.winfo_children()[0]
            label_widget.configure(text=f"{label}: {var.get()}%")

        var.trace_add("write", update_label)

    def _build_gauge(self, parent, label, var):
        frame = ttk.Frame(parent, style="Mission.TFrame")
        frame.pack(fill="x", pady=8)
        ttk.Label(frame, text=label, style="Mission.TLabel").pack(anchor="w")
        bar = ttk.Progressbar(
            frame,
            style="Mission.Horizontal.TProgressbar",
            maximum=100,
            variable=var,
        )
        bar.pack(fill="x", pady=4)

    def _update_outputs(self):
        state = MissionState(
            oxygen=self.oxygen_var.get(),
            power=self.power_var.get(),
            food=self.food_var.get(),
            fuel=self.fuel_var.get(),
            hull=self.hull_var.get(),
        )
        goal_text = self.goal_text_var.get().strip() or "Reach Destination"
        goal_days = max(1, self.goal_days_var.get())

        strategy = self.engine.generate_strategy(state, goal_text, goal_days)

        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", strategy)
        self.output.configure(state="disabled")

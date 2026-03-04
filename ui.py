import tkinter as tk
from tkinter import ttk

from mission_state import CargoInventory, MissionState
from reasoning_engine import ReasoningEngine


class MissionControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Autonomous Space Mission Survival Agent")
        self.geometry("1200x720")
        self.configure(bg="black")

        self.engine = ReasoningEngine()
        self.last_events = []

        # Variables
        self.oxygen_var = tk.IntVar(value=80)
        self.power_var = tk.IntVar(value=70)
        self.food_var = tk.IntVar(value=75)
        self.fuel_var = tk.IntVar(value=65)
        self.hull_var = tk.IntVar(value=90)

        self.oxygen_reserve_var = tk.IntVar(value=60)
        self.power_reserve_var = tk.IntVar(value=55)
        self.food_reserve_var = tk.IntVar(value=65)
        self.fuel_reserve_var = tk.IntVar(value=50)
        self.hull_plates_var = tk.IntVar(value=40)

        self.autopilot_var = tk.IntVar(value=1)
        self.sim_run_var = tk.IntVar(value=1)
        self.sim_speed_var = tk.IntVar(value=3)

        self.goal_text_var = tk.StringVar(value="Reach Mars")
        self.goal_days_var = tk.IntVar(value=20)

        # Drone movement state
        self.drone_target = None
        self.drone_speed = 4

        self._build_styles()
        self._build_layout()
        self._update_outputs()
        self._tick()

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

        ttk.Label(left, text="Drone & Simulation", style="Mission.TLabel").pack(
            anchor="w", pady=(8, 2)
        )

        autopilot = tk.Checkbutton(
            left,
            text="Autopilot Active",
            variable=self.autopilot_var,
            bg="black",
            fg="#00f5ff",
            selectcolor="black",
            activebackground="black",
            activeforeground="#00f5ff",
        )
        autopilot.pack(anchor="w")

        sim_run = tk.Checkbutton(
            left,
            text="Auto-Sim Running",
            variable=self.sim_run_var,
            bg="black",
            fg="#00f5ff",
            selectcolor="black",
            activebackground="black",
            activeforeground="#00f5ff",
        )
        sim_run.pack(anchor="w")

        ttk.Label(left, text="Sim Speed", style="Mission.TLabel").pack(anchor="w")
        speed = tk.Scale(
            left,
            from_=1,
            to=8,
            orient="horizontal",
            variable=self.sim_speed_var,
            bg="black",
            fg="#00f5ff",
            highlightthickness=0,
            troughcolor="#111",
            activebackground="#00f5ff",
        )
        speed.pack(fill="x", pady=(0, 8))

        ttk.Label(left, text="Cargo Reserves", style="Mission.TLabel").pack(
            anchor="w", pady=(6, 2)
        )
        self._build_spinbox(left, "Oxygen Reserve", self.oxygen_reserve_var)
        self._build_spinbox(left, "Power Cells", self.power_reserve_var)
        self._build_spinbox(left, "Food Reserve", self.food_reserve_var)
        self._build_spinbox(left, "Fuel Reserve", self.fuel_reserve_var)
        self._build_spinbox(left, "Hull Plates", self.hull_plates_var)

        # Center: Gauges + Drone Area
        center = ttk.Frame(main, style="Mission.TFrame")
        center.grid(row=0, column=1, sticky="nsew", padx=12)

        ttk.Label(center, text="System Gauges", style="Mission.TLabel").pack(anchor="w")
        self._build_gauge(center, "Oxygen", self.oxygen_var)
        self._build_gauge(center, "Power", self.power_var)
        self._build_gauge(center, "Food", self.food_var)
        self._build_gauge(center, "Fuel", self.fuel_var)
        self._build_gauge(center, "Hull Integrity", self.hull_var)

        ttk.Label(center, text="Astronaut Drone Zone", style="Mission.TLabel").pack(
            anchor="w", pady=(12, 2)
        )
        self._build_drone_zone(center)

        # Right: Output
        right = ttk.Frame(main, style="Mission.TFrame")
        right.grid(row=0, column=2, sticky="nsew", padx=(12, 0))

        ttk.Label(right, text="Strategic Output", style="Mission.TLabel").pack(anchor="w")
        self.output = tk.Text(
            right,
            height=30,
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
            self.oxygen_reserve_var,
            self.power_reserve_var,
            self.food_reserve_var,
            self.fuel_reserve_var,
            self.hull_plates_var,
            self.autopilot_var,
            self.sim_run_var,
            self.sim_speed_var,
            self.goal_text_var,
            self.goal_days_var,
        ]:
            var.trace_add("write", lambda *args: self._update_outputs())

    def _build_drone_zone(self, parent):
        frame = ttk.Frame(parent, style="Mission.TFrame")
        frame.pack(fill="both", expand=False)

        self.canvas = tk.Canvas(
            frame,
            width=320,
            height=220,
            bg="#050505",
            highlightthickness=1,
            highlightbackground="#00f5ff",
        )
        self.canvas.pack(fill="x")

        self.canvas.create_text(60, 200, text="Dock", fill="#00f5ff", font=("Consolas", 9))
        self.canvas.create_oval(40, 170, 80, 210, outline="#00f5ff")

        stations = [
            (260, 40, "O2"),
            (60, 40, "PWR"),
            (260, 180, "FOOD"),
            (160, 40, "FUEL"),
            (160, 180, "HULL"),
        ]
        for x, y, label in stations:
            self.canvas.create_oval(x - 16, y - 16, x + 16, y + 16, outline="#00ff88")
            self.canvas.create_text(x, y, text=label, fill="#00ff88", font=("Consolas", 9))

        # Drone starts at dock.
        self.drone = self.canvas.create_oval(52, 182, 68, 198, fill="#00f5ff", outline="")
        self.drone_position = [60, 190]

        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self._animate_drone()

    def _on_canvas_click(self, event):
        # Set a new target for the drone to move toward.
        self.drone_target = [event.x, event.y]

    def _animate_drone(self):
        if self.drone_target:
            dx = self.drone_target[0] - self.drone_position[0]
            dy = self.drone_target[1] - self.drone_position[1]
            distance = (dx * dx + dy * dy) ** 0.5

            if distance <= self.drone_speed:
                self.drone_position = self.drone_target
                self.drone_target = None
            else:
                self.drone_position[0] += self.drone_speed * dx / distance
                self.drone_position[1] += self.drone_speed * dy / distance

            x, y = self.drone_position
            self.canvas.coords(self.drone, x - 8, y - 8, x + 8, y + 8)

        self.after(30, self._animate_drone)

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

    def _build_spinbox(self, parent, label, var):
        frame = ttk.Frame(parent, style="Mission.TFrame")
        frame.pack(fill="x", pady=4)
        ttk.Label(frame, text=label, style="Mission.TLabel").pack(anchor="w")
        box = tk.Spinbox(
            frame,
            from_=0,
            to=100,
            textvariable=var,
            bg="#111",
            fg="#00f5ff",
            insertbackground="#00f5ff",
            relief="flat",
            width=6,
            command=self._update_outputs,
        )
        box.pack(anchor="w")

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

    def _tick(self):
        if self.sim_run_var.get() == 1:
            state = MissionState(
                oxygen=self.oxygen_var.get(),
                power=self.power_var.get(),
                food=self.food_var.get(),
                fuel=self.fuel_var.get(),
                hull=self.hull_var.get(),
            )
            cargo = CargoInventory(
                oxygen_reserve=self.oxygen_reserve_var.get(),
                power_reserve=self.power_reserve_var.get(),
                food_reserve=self.food_reserve_var.get(),
                fuel_reserve=self.fuel_reserve_var.get(),
                hull_plates=self.hull_plates_var.get(),
            )

            state, cargo, events = self.engine.simulate_tick(
                state,
                cargo,
                speed=self.sim_speed_var.get(),
                autopilot=bool(self.autopilot_var.get()),
            )

            self.last_events = events
            self.oxygen_var.set(state.oxygen)
            self.power_var.set(state.power)
            self.food_var.set(state.food)
            self.fuel_var.set(state.fuel)
            self.hull_var.set(state.hull)

            self.oxygen_reserve_var.set(cargo.oxygen_reserve)
            self.power_reserve_var.set(cargo.power_reserve)
            self.food_reserve_var.set(cargo.food_reserve)
            self.fuel_reserve_var.set(cargo.fuel_reserve)
            self.hull_plates_var.set(cargo.hull_plates)

        self._update_outputs()
        self.after(1000, self._tick)

    def _update_outputs(self):
        state = MissionState(
            oxygen=self.oxygen_var.get(),
            power=self.power_var.get(),
            food=self.food_var.get(),
            fuel=self.fuel_var.get(),
            hull=self.hull_var.get(),
        )
        cargo = CargoInventory(
            oxygen_reserve=self.oxygen_reserve_var.get(),
            power_reserve=self.power_reserve_var.get(),
            food_reserve=self.food_reserve_var.get(),
            fuel_reserve=self.fuel_reserve_var.get(),
            hull_plates=self.hull_plates_var.get(),
        )
        goal_text = self.goal_text_var.get().strip() or "Reach Destination"
        goal_days = max(1, self.goal_days_var.get())

        strategy = self.engine.generate_strategy(
            state,
            cargo,
            goal_text,
            goal_days,
            autopilot=bool(self.autopilot_var.get()),
            last_events=self.last_events,
        )

        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", strategy)
        self.output.configure(state="disabled")

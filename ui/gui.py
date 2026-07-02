# ui/gui.py
import tkinter as tk
from tkinter import ttk
from core.solver import solve
from core.components import Resistor, VoltageSource
from ui.circuits import CIRCUITS


class CircuitApp:
    def __init__(self, root):
        root.title("Circuit Simulator")

        panel = tk.Frame(root)
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(panel, text="Circuit:").pack(anchor="w")
        self.selector = ttk.Combobox(panel, values=list(CIRCUITS.keys()),
                                     state="readonly", width=20)
        self.selector.current(0)
        self.selector.pack(anchor="w", pady=(0, 10))
        self.selector.bind("<<ComboboxSelected>>", lambda e: self.solve_and_draw())

        tk.Button(panel, text="Solve", command=self.solve_and_draw).pack()
        self.status = tk.Label(panel, text="", fg="red", wraplength=150)
        self.status.pack(pady=10)

        self.canvas = tk.Canvas(root, width=620, height=360, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)

        self.solve_and_draw()

    def solve_and_draw(self):
        circuit = CIRCUITS[self.selector.get()]
        try:
            voltages, currents = solve(circuit["components"])
            self.status.config(text="")
        except ValueError as err:
            self.status.config(text=str(err))
            return
        self.draw(circuit, voltages, currents)

    def draw(self, circuit, voltages, currents):
        c = self.canvas
        c.delete("all")
        pos = circuit["positions"]

        # --- components: line between nodes + symbol at midpoint ---
        for comp in circuit["components"]:
            (x1, y1), (x2, y2) = pos[comp.nodes[0]], pos[comp.nodes[1]]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2

            c.create_line(x1, y1, x2, y2)

            if isinstance(comp, Resistor):
                c.create_rectangle(mx - 28, my - 11, mx + 28, my + 11,
                                   fill="white")
                c.create_text(mx, my, text=f"{comp.id}={comp.value:g}Ω",
                              font=("TkDefaultFont", 9))
            elif isinstance(comp, VoltageSource):
                r = 16
                c.create_oval(mx - r, my - r, mx + r, my + r, fill="white")
                c.create_text(mx, my - 5, text="+")
                c.create_text(mx, my + 6, text="−")
                label = (f"{comp.id}={comp.value:g}V  "
                         f"I={abs(currents[comp.id]):.3f}A")
                c.create_text(mx, my + r + 12, text=label,
                              fill="darkgreen", font=("TkDefaultFont", 9))

        # --- nodes: dot + voltage label ---
        for name, (x, y) in pos.items():
            c.create_oval(x - 4, y - 4, x + 4, y + 4, fill="black")
            c.create_text(x, y - 16,
                          text=f"{name}: {voltages.get(name, 0.0):.2f}V",
                          fill="blue", font=("TkDefaultFont", 10, "bold"))

        # ground symbol at GND's position
        if "GND" in pos:
            gx, gy = pos["GND"]
            c.create_line(gx - 20, gy + 8, gx + 20, gy + 8, width=3)
            c.create_line(gx - 13, gy + 15, gx + 13, gy + 15, width=2)
            c.create_line(gx - 6, gy + 22, gx + 6, gy + 22, width=1)
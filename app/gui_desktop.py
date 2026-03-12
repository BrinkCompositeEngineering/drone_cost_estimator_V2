import tkinter as tk
from tkinter import ttk

from components.component import Component
from app.estimator_engine import EstimatorEngine


class DroneEstimatorGUI:

    def __init__(self):

        self.engine = EstimatorEngine()

        self.root = tk.Tk()
        self.root.title("Drone Tooling Cost Estimator")

        self.components = []

        self.create_widgets()

    def create_widgets(self):

        frame = ttk.Frame(self.root, padding=10)
        frame.grid()

        ttk.Label(frame, text="Component Name").grid(row=0, column=0)
        ttk.Label(frame, text="Length (mm)").grid(row=0, column=1)
        ttk.Label(frame, text="Width (mm)").grid(row=0, column=2)
        ttk.Label(frame, text="Thickness (mm)").grid(row=0, column=3)

        self.name = ttk.Entry(frame)
        self.length = ttk.Entry(frame)
        self.width = ttk.Entry(frame)
        self.thickness = ttk.Entry(frame)

        self.name.grid(row=1, column=0)
        self.length.grid(row=1, column=1)
        self.width.grid(row=1, column=2)
        self.thickness.grid(row=1, column=3)

        ttk.Button(frame, text="Add Component", command=self.add_component).grid(row=2, column=0)
        ttk.Button(frame, text="Calculate", command=self.calculate).grid(row=2, column=1)

        self.output = tk.Text(frame, height=15, width=80)
        self.output.grid(row=3, column=0, columnspan=4)

    def add_component(self):

        comp = Component(
            self.name.get(),
            int(self.length.get()),
            int(self.width.get()),
            int(self.thickness.get())
        )

        self.components.append(comp)

        self.output.insert(tk.END, f"Added: {comp.name}\n")

    def calculate(self):

        total = 0

        for comp in self.components:

            result = self.engine.process_component(comp)

            total += result["component_cost"]

            self.output.insert(
                tk.END,
                f"{result['name']} cost: {result['component_cost']}\n"
            )

        self.output.insert(tk.END, f"\nTOTAL PROJECT COST: {total}\n")

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":

    app = DroneEstimatorGUI()
    app.run()
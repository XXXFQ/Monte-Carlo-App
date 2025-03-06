import tkinter as tk
from tkinter import ttk
import random
import math

class Application(ttk.Frame):
    def __init__(self, master=None):
        '''
        Initialize the application with the given master window.
        
        Parameters:
            master (tk.Tk): The master window for the application.
        
        Attributes:
            master (tk.Tk): The master window for the application.
            num_points_label (tk.Label): Label for the number of points entry.
            num_points_entry (tk.Entry): Entry for the number of points.
            run_button (tk.Button): Button to run the simulation.
            result_label (tk.Label): Label to display the result.
            canvas_width (int): Width of the canvas for drawing the simulation.
            canvas_height (int): Height of the canvas for drawing the simulation.
            canvas (tk.Canvas): Canvas for drawing the simulation.
        '''
        super().__init__(master)
        self.master = master
        master.title("Monte Carlo Simulation")
        
        # Controls for the simulation
        self.num_points_label = tk.Label(master, text="Number of Points:")
        self.num_points_label.grid(row=0, column=0)
        
        self.num_points_entry = tk.Entry(master)
        self.num_points_entry.insert(0, "1000")
        self.num_points_entry.grid(row=0, column=1)
        
        self.run_button = tk.Button(master, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=1, column=0, columnspan=2)
        
        self.result_label = tk.Label(master, text="Result: ")
        self.result_label.grid(row=2, column=0, columnspan=2)
        
        # Canvas for drawing the simulation
        self.canvas_width = 300
        self.canvas_height = 300
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Draw the circle (inscribed in the square)
        # The simulation uses points in [-1,1] so the circle's bounding box in simulation coordinates is (-1,-1) to (1,1)
        # Transform these to canvas coordinates: (-1, 1) -> (0, 0) and (1, -1) -> (canvas_width, canvas_height)
        self.canvas.create_oval(0, 0, self.canvas_width, self.canvas_height, outline="blue", width=2)
    
    def run_simulation(self):
        '''
        Run the Monte Carlo simulation to estimate Pi.
        '''
        try:
            num_points = int(self.num_points_entry.get())
        except ValueError:
            self.result_label.config(text="Invalid input. Please enter an integer.")
            return
        
        inside_circle = 0
        
        # Remove previously drawn points (keep the circle)
        self.canvas.delete("point")
        
        for _ in range(num_points):
            # Generate points in the square [-1, 1] x [-1, 1]
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            distance = math.sqrt(x**2 + y**2)
            if distance <= 1:
                inside_circle += 1
                color = "green"
            else:
                color = "red"
            
            # Transform simulation coordinates (x,y) to canvas coordinates.
            # Here (0,0) in simulation maps to the center of the canvas.
            canvas_x = (x + 1) * self.canvas_width / 2
            canvas_y = (1 - y) * self.canvas_height / 2  # Invert y-axis for proper orientation
            # Draw a small circle (dot) for each point
            r = 1  # radius of the point
            self.canvas.create_oval(canvas_x - r, canvas_y - r, canvas_x + r, canvas_y + r,
                                    fill=color, outline=color, tags="point")
        
        pi_estimate = 4 * inside_circle / num_points
        self.result_label.config(text="Estimated Pi: " + str(pi_estimate))

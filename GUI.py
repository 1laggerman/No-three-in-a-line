import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from package.Grid import Grid as Grid

# Define the main application class
class GridConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grid Configuration Tool")
        self.geometry("1080x720")  # Wider window to accommodate the plot
        self.is_range = False

        # Initialize the user interface
        self.create_widgets()
        self.create_plot()

    def create_widgets(self):
        # Configuration Frame on the Left
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Toggle Button
        self.toggle_button = ttk.Button(left_frame, text="Analysis Mode", command=self.toggle_input_mode)
        self.toggle_button.grid(row=0, column=0, padx=10, pady=10)

        # Grid Configuration
        self.config_frame = ttk.LabelFrame(left_frame, text="Grid Configuration")
        self.config_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        # self.init_single_value_inputs()
        
        ttk.Label(self.config_frame, text="n:").grid(row=0, column=0, padx=5, pady=5)
        self.n_input = ttk.Entry(self.config_frame, width=10)
        self.n_input.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.config_frame, text="d:").grid(row=1, column=0, padx=5, pady=5)
        self.d_input = ttk.Entry(self.config_frame, width=10)
        self.d_input.grid(row=1, column=1, padx=5, pady=5)

        # Algorithm Selection
        self.algo_frame = ttk.LabelFrame(left_frame, text="Select Algorithm")
        self.algo_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.algo_var = tk.StringVar()
        ttk.Radiobutton(self.algo_frame, text="Find Max Solutions", value="max_solutions", variable=self.algo_var).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(self.algo_frame, text="Random Greedy", value="random_greedy", variable=self.algo_var).grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(self.algo_frame, text="Min Conflict", value="min_conflict", variable=self.algo_var).grid(row=2, column=0, sticky="w")

        # Run Button
        self.run_button = ttk.Button(left_frame, text="Run", command=self.run_algorithm)
        self.run_button.grid(row=3, column=0, padx=10, pady=10)
        
    def toggle_input_mode(self):
        # Clear existing widgets
        for widget in self.config_frame.winfo_children():
            widget.destroy()

        if not self.toggle_button.config('text')[-1] == 'Single Run Mode':
            # Switch to range inputs using entry fields
            self.init_range_inputs()
            self.toggle_button.config(text='Single Run Mode')
        else:
            # Switch back to single value inputs
            self.init_single_value_inputs()
            self.toggle_button.config(text='Analysis Mode')
            
    def init_single_value_inputs(self):
        ttk.Label(self.config_frame, text="n:").grid(row=0, column=0, padx=5, pady=5)
        self.n_input = ttk.Entry(self.config_frame, width=10)
        self.n_input.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.config_frame, text="d:").grid(row=1, column=0, padx=5, pady=5)
        self.d_input = ttk.Entry(self.config_frame, width=10)
        self.d_input.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.config_frame, text="k:").grid(row=2, column=0, padx=5, pady=5)
        self.k_input = ttk.Entry(self.config_frame, width=10)
        self.k_input.grid(row=2, column=1, padx=5, pady=5)
            
    def init_range_inputs(self):
        for var, row in [('n', 0), ('d', 3), ('k', 6)]:
            ttk.Label(self.config_frame, text=f"{var} range:").grid(row=row, column=0, padx=5, pady=5, columnspan=2)
            min_label = ttk.Label(self.config_frame, text="Min:")
            min_label.grid(row=row+1, column=0, padx=5, pady=2)
            min_entry = ttk.Entry(self.config_frame, width=10)
            min_entry.grid(row=row+1, column=1, padx=5, pady=2)
            max_label = ttk.Label(self.config_frame, text="Max:")
            max_label.grid(row=row+1, column=2, padx=5, pady=2)
            max_entry = ttk.Entry(self.config_frame, width=10)
            max_entry.grid(row=row+1, column=3, padx=5, pady=2)

    def create_plot(self):
        # Plotting Frame on the Right
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        # Placeholder for Matplotlib Figure
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)  # Adding a subplot
        self.ax.grid(True)  # Enable grid
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def run_algorithm(self):
        n = int(self.n_input.get())
        d = int(self.d_input.get())
        k = int(self.k_input.get())
        
        g = Grid(n, d)
        
        algorithm = self.algo_var.get()
        
        gp = None
        
        if algorithm =='max_solutions':
            # self.run_max_solutions(n, d)
            pass
        elif algorithm == 'random_greedy':
            gp = g.random_greedy(allowed_in_line=k)
        elif algorithm =='min_conflict':
            gp = g.min_conflict(allowed_in_line=k)
            
        

        # Example of plotting something based on the algorithm
        # Clear the current plot
        self.ax.clear()
        self.ax.grid(True)

        # Here you would include your actual algorithm logic and plotting
        self.ax.plot([0, n], [0, d], label="Example Line")
        self.ax.legend()

        # Refresh the plot
        self.canvas.draw()

# Create and run the application
app = GridConfigApp()
app.mainloop()

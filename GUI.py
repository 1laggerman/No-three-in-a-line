import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from package.Grid import Grid as Grid
from package.statistics import plot_line, run_and_save, run_linear, scatter, RunData

# Define the main application class
class GridConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grid Configuration Tool")
        self.geometry("1080x720")  # Wider window to accommodate the plot
        self.is_range = False
        self.range_inputs = {}
        self.protocol("WM_DELETE_WINDOW", self.exit)

        # Initialize the user interface
        self.create_widgets()
        self.create_plot()

    def create_widgets(self):
        # Configuration Frame on the Left
        self.left_frame = ttk.Frame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Toggle Button
        self.toggle_button = ttk.Button(self.left_frame, text="Analysis Mode", command=self.toggle_input_mode)
        self.toggle_button.grid(row=0, column=0, padx=10, pady=10)

        # Grid Configuration
        self.config_frame = ttk.LabelFrame(self.left_frame, text="Grid Configuration")
        self.config_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        # self.init_single_value_inputs()
        
        ttk.Label(self.config_frame, text="n:").grid(row=0, column=0, padx=5, pady=5)
        self.n_input = ttk.Entry(self.config_frame, width=10)
        self.n_input.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.config_frame, text="d:").grid(row=1, column=0, padx=5, pady=5)
        self.d_input = ttk.Entry(self.config_frame, width=10)
        self.d_input.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.config_frame, text="k:").grid(row=2, column=0, padx=5, pady=5)
        self.k_input = ttk.Entry(self.config_frame, width=10)
        self.k_input.grid(row=2, column=1, padx=5, pady=5)

        # Algorithm Selection
        self.algo_frame = ttk.LabelFrame(self.left_frame, text="Select Algorithm")
        self.algo_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.algo_var = tk.StringVar()
        ttk.Radiobutton(self.algo_frame, text="Find Max Solutions", value="max_solutions", variable=self.algo_var, command = lambda : self.show_args()).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(self.algo_frame, text="Random Greedy", value="random_greedy", variable=self.algo_var, command = lambda : self.show_args()).grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(self.algo_frame, text="Min Conflict", value="min_conflict", variable=self.algo_var, command = lambda : self.show_args()).grid(row=2, column=0, sticky="w")
        
        self.args_frame = ttk.LabelFrame(self.left_frame, text="Enter Arguments")
        self.args_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Run Button
        self.run_button = ttk.Button(self.left_frame, text="Run", command=self.run_algorithm)
        self.run_button.grid(row=4, column=0, padx=10, pady=10)

    def show_args(self):
        self.args_frame.destroy()
        self.args_frame = ttk.LabelFrame(self.left_frame, text="Enter Arguments")
        self.args_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        selected = self.algo_var.get()
        for widget in self.args_frame.winfo_children():
            widget.destroy()
        if selected == "Find Max Solutions":
            self.args_max_solutions()
        elif selected == "Random Greedy":
            self.args_random_greedy()
        elif selected == "min_conflict":
            self.args_min_conflict()
        
    def args_random_greedy(self):
        return
    
    def args_min_conflict(self):
        ttk.Label(self.args_frame, text="max_iters:").grid(row=0, column=0, padx=5, pady=5)
        self.max_iter_input = ttk.Entry(self.args_frame, width=10)
        self.max_iter_input.grid(row=0, column=1, padx=5, pady=5)
        
    def toggle_input_mode(self):
        # Clear existing widgets
        for widget in self.config_frame.winfo_children():
            widget.destroy()
        self.range_inputs.clear()

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
            ttk.Label(self.config_frame, text=f"{var} range:").grid(row=row, column=0, padx=5, pady=5, columnspan=3)
            min_label = ttk.Label(self.config_frame, text="Min:")
            min_label.grid(row=row+1, column=0, padx=5, pady=2)
            min_entry = ttk.Entry(self.config_frame, width=10)
            min_entry.grid(row=row+1, column=1, padx=5, pady=2)
            max_label = ttk.Label(self.config_frame, text="Max:")
            max_label.grid(row=row+1, column=2, padx=5, pady=2)
            max_entry = ttk.Entry(self.config_frame, width=10)
            max_entry.grid(row=row+1, column=3, padx=5, pady=2)
            
            self.range_inputs[var] = {'min': min_entry, 'max': max_entry}

    def create_plot(self):
        # Plotting Frame on the Right
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        

        # Placeholder for Matplotlib Figure
        size = self.winfo_height()
        try:
            d = int(self.d_input.get())
        except:
            d = 2
            pass
        self.figure, self.ax = plt.subplots(figsize=((size * 1.2) / 80, size / 80), dpi=80, subplot_kw={'projection': '3d'} if d == 3 else None)
        self.ax.grid(True)  # Enable grid
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def run_algorithm(self):
        algorithm = self.algo_var.get()
        
        if self.toggle_button.config('text')[-1] == 'Single Run Mode':
            values = {}
            for var, entries in self.range_inputs.items():
                min_value = int(entries['min'].get())
                max_value = int(entries['max'].get())
                values[var] = (min_value, max_value, True if min_value < max_value else False)
                
            ks = range(values['k'][0], values['k'][1]+1)
            runner = 'k'
            ds = range(values['d'][0], values['d'][1]+1)
            if values['d'][2] == True:
                runner = 'd'
            ns = range(values['n'][0], values['n'][1]+1)
            if values['n'][2] == True:
                runner = 'n'
                
            if algorithm == 'max_solutions':
                pass
            elif algorithm == 'random_greedy':
                data = run_linear(func=Grid.random_greedy, ns=ns, ds=ds, ks=ks)
            elif algorithm == 'min_conflict':
                kwargs = {"max_iter": int(self.max_iter_input.get())}
                data = run_linear(func=Grid.min_conflict, ns=ns, ds=ds, ks=ks, **kwargs)
                
            
            scatter(data)
                    
        else:
            self.create_plot()
            n = int(self.n_input.get())
            d = int(self.d_input.get())
            k = int(self.k_input.get())
            g = Grid(n, d)
            gp = None
            
            if algorithm == 'max_solutions':
                # self.run_max_solutions(n, d)
                pass
            elif algorithm == 'random_greedy':
                gp = g.random_greedy(allowed_in_line=k)
            elif algorithm == 'min_conflict':
                kwargs = {"max_iter": int(self.max_iter_input.get())}
                gp = g.min_conflict(allowed_in_line=k, **kwargs)
                
            # Clear the current plot
            self.ax.clear()
            self.ax.grid(True)
            g.make_grid(self.ax, gp)

        self.canvas.draw()
        
    def exit(self):
        self.destroy()
        exit(0)

# Create and run the application
app = GridConfigApp()
app.mainloop()

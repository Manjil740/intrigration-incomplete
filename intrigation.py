import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sympy as sp
from sympy import Eq, Derivative, Integral, pretty_print, latex, series, limit, solveset
from PIL import Image, ImageTk
import webbrowser
import os
import platform
import re
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from io import BytesIO
import threading
from queue import Queue
import time
import pickle
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

class AdvancedMathSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculus Solver Pro")
        self.root.geometry("1200x900")
        self.root.minsize(1000, 800)
        
        # Initialize variables
        self.operation_var = tk.StringVar(value="Derivative")
        self.order_var = tk.StringVar(value="1")
        self.definite_var = tk.BooleanVar(value=False)
        self.lower_limit_var = tk.StringVar(value="0")
        self.upper_limit_var = tk.StringVar(value="1")
        self.plot_range_var = tk.StringVar(value="Auto")
        self.custom_min_var = tk.StringVar(value="-5")
        self.custom_max_var = tk.StringVar(value="5")
        self.dark_mode_var = tk.BooleanVar(value=False)
        self.history = []
        self.current_problem = ""
        self.plot_img = None
        self.plot_canvas = None
        self.result_queue = Queue()
        self.transformations = (standard_transformations + (implicit_multiplication_application,))
        
        # Configure style
        self.configure_styles()
        
        # Create main container with paned window for resizing
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Top panel for input and controls
        self.top_panel = ttk.Frame(self.main_paned)
        self.main_paned.add(self.top_panel, weight=1)
        
        # Bottom panel for results and plots
        self.bottom_panel = ttk.Frame(self.main_paned)
        self.main_paned.add(self.bottom_panel, weight=2)
        
        # Application title
        self.title_label = ttk.Label(self.top_panel, 
                                   text="Advanced Calculus Solver Pro", 
                                   font=('Arial', 20, 'bold'))
        self.title_label.pack(pady=(10, 20))
        
        # Create input widgets
        self.create_input_widgets()
        
        # Create operation selection
        self.create_operation_selection()
        
        # Create symbol buttons with better organization
        self.create_symbol_buttons()
        
        # Create solve and clear buttons
        self.create_action_buttons()
        
        # Create result display with tabs
        self.create_result_display()
        
        # Create examples section with categories
        self.create_examples_section()
        
        # Create credits and help section
        self.create_credits_section() 
        
        # Load history if exists
        self.load_history()
        
        # Check for results in queue periodically
        self.root.after(100, self.process_result_queue)

    def configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Light mode configuration
        self.style.configure('.', background='#f0f0f0', foreground='black')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12), padding=5)
        self.style.configure('TRadiobutton', background='#f0f0f0', font=('Arial', 12))
        self.style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'))
        self.style.map('TButton', background=[('active', '#e0e0e0')])
        self.style.configure('Accent.TButton', background='#4CAF50', foreground='white')
        self.style.map('Accent.TButton', background=[('active', '#45a049')])
        self.style.configure('TEntry', fieldbackground='white')
        self.style.configure('TText', background='white', foreground='black')

    def create_input_widgets(self):
        # Main input frame
        input_frame = ttk.LabelFrame(self.top_panel, text="Problem Input", padding=10)
        input_frame.pack(fill=tk.X, pady=5, padx=10)
        
        # Expression input
        expr_frame = ttk.Frame(input_frame)
        expr_frame.pack(fill=tk.X, pady=5)
        
        self.expression_label = ttk.Label(expr_frame, text="Mathematical Expression:")
        self.expression_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.entry_expression = ttk.Entry(expr_frame, width=40, font=('Arial', 12))
        self.entry_expression.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.entry_expression.bind("<Return>", lambda e: self.on_solve_click())
        
        # Variable and options frame
        options_frame = ttk.Frame(input_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        # Variable input
        var_frame = ttk.Frame(options_frame)
        var_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        self.variable_label = ttk.Label(var_frame, text="Variable:")
        self.variable_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.entry_variable = ttk.Entry(var_frame, width=5, font=('Arial', 12))
        self.entry_variable.pack(side=tk.LEFT)
        self.entry_variable.insert(0, "x")
        
        # Derivative order input
        self.order_frame = ttk.Frame(options_frame)
        self.order_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        self.order_label = ttk.Label(self.order_frame, text="Order:")
        self.order_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.entry_order = ttk.Entry(self.order_frame, width=3, font=('Arial', 12), textvariable=self.order_var)
        self.entry_order.pack(side=tk.LEFT)
        
        # Integral limits frame (initially hidden)
        self.limits_frame = ttk.Frame(options_frame)
        
        self.definite_check = ttk.Checkbutton(options_frame, text="Definite Integral", 
                                            variable=self.definite_var, 
                                            command=self.toggle_definite_integral)
        self.definite_check.pack(side=tk.LEFT, padx=(0, 10))
        
        # Plot range selection
        self.plot_range_frame = ttk.Frame(options_frame)
        self.plot_range_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        ttk.Label(self.plot_range_frame, text="Plot Range:").pack(side=tk.LEFT)
        self.plot_range_combo = ttk.Combobox(self.plot_range_frame, 
                                           textvariable=self.plot_range_var,
                                           values=["Auto", "Custom"],
                                           state="readonly",
                                           width=8)
        self.plot_range_combo.pack(side=tk.LEFT, padx=(5, 0))
        self.plot_range_combo.bind("<<ComboboxSelected>>", self.toggle_plot_range)
        
        self.custom_range_frame = ttk.Frame(self.plot_range_frame)
        
        # Update UI based on initial operation
        self.update_operation_ui()

    def toggle_plot_range(self, event=None):
        if self.plot_range_var.get() == "Custom":
            self.custom_range_frame.pack(side=tk.LEFT, padx=(5, 0))
            
            # Clear any existing widgets
            for widget in self.custom_range_frame.winfo_children():
                widget.destroy()
            
            ttk.Label(self.custom_range_frame, text="From:").pack(side=tk.LEFT)
            self.entry_plot_min = ttk.Entry(self.custom_range_frame, width=5, 
                                          font=('Arial', 12), textvariable=self.custom_min_var)
            self.entry_plot_min.pack(side=tk.LEFT, padx=(0, 5))
            
            ttk.Label(self.custom_range_frame, text="To:").pack(side=tk.LEFT)
            self.entry_plot_max = ttk.Entry(self.custom_range_frame, width=5, 
                                          font=('Arial', 12), textvariable=self.custom_max_var)
            self.entry_plot_max.pack(side=tk.LEFT)
        else:
            self.custom_range_frame.pack_forget()

    def create_operation_selection(self):
        frame = ttk.LabelFrame(self.top_panel, text="Operation", padding=10)
        frame.pack(fill=tk.X, pady=10, padx=10)
        
        operations = [
            ("Derivative", "Calculate derivatives of functions"),
            ("Integral", "Calculate definite or indefinite integrals"),
            ("Limit", "Find limits of functions"),
            ("Series", "Expand functions as Taylor series"),
            ("Solve", "Solve equations algebraically")
        ]
        
        for i, (op_text, op_desc) in enumerate(operations):
            radio = ttk.Radiobutton(frame, 
                                  text=op_text, 
                                  variable=self.operation_var, 
                                  value=op_text,
                                  command=self.update_operation_ui)
            radio.pack(side=tk.LEFT, padx=(0, 15))
            
            # Add tooltip for description
            self.create_tooltip(radio, op_desc)

    def create_tooltip(self, widget, text):
        tooltip = ttk.Label(self.root, text=text, background="#ffffe0", relief="solid", 
                          borderwidth=1, padding=5, font=('Arial', 10))
        tooltip.pack_forget()
        
        def enter(event):
            x = widget.winfo_rootx() + widget.winfo_width() + 5
            y = widget.winfo_rooty()
            tooltip.lift()
            tooltip.place(x=x, y=y)
            
        def leave(event):
            tooltip.place_forget()
            
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def update_operation_ui(self):
        operation = self.operation_var.get()
        
        # Hide all optional frames first
        self.order_frame.pack_forget()
        self.definite_check.pack_forget()
        self.limits_frame.pack_forget()
        
        if operation == "Derivative":
            self.order_frame.pack(side=tk.LEFT, padx=(0, 20))
            self.order_label.config(text="Order:")
            self.order_var.set("1")
        elif operation == "Integral":
            self.definite_check.pack(side=tk.LEFT, padx=(0, 10))
            if self.definite_var.get():
                self.show_integral_limits()
        elif operation == "Limit":
            self.order_frame.pack(side=tk.LEFT, padx=(0, 20))
            self.order_label.config(text="Point:")
            self.order_var.set("0")
        elif operation == "Series":
            self.order_frame.pack(side=tk.LEFT, padx=(0, 20))
            self.order_label.config(text="Order:")
            self.order_var.set("5")
        elif operation == "Solve":
            pass  # No additional options needed for solving

    def toggle_definite_integral(self):
        if self.definite_var.get():
            self.show_integral_limits()
        else:
            self.limits_frame.pack_forget()

    def show_integral_limits(self):
        self.limits_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        # Clear any existing widgets
        for widget in self.limits_frame.winfo_children():
            widget.destroy()
        
        # Lower limit
        ttk.Label(self.limits_frame, text="From:").pack(side=tk.LEFT)
        self.entry_lower = ttk.Entry(self.limits_frame, width=5, font=('Arial', 12), 
                                   textvariable=self.lower_limit_var)
        self.entry_lower.pack(side=tk.LEFT, padx=(0, 10))
        
        # Upper limit
        ttk.Label(self.limits_frame, text="To:").pack(side=tk.LEFT)
        self.entry_upper = ttk.Entry(self.limits_frame, width=5, font=('Arial', 12), 
                                   textvariable=self.upper_limit_var)
        self.entry_upper.pack(side=tk.LEFT)

    def create_symbol_buttons(self):
        frame = ttk.LabelFrame(self.top_panel, text="Symbols & Functions", padding=10)
        frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Organize buttons in categories
        categories = [
            ("Calculus", [
                ("∫", self.insert_integration_symbol),
                ("d/dx", self.insert_derivative_symbol),
                ("∂/∂x", lambda: self.insert_symbol("diff(, )")),  # Partial derivative
                ("lim", lambda: self.insert_symbol("limit(, , )"))
            ]),
            ("Operators", [
                ("^", self.insert_power_operator),
                ("√", lambda: self.insert_symbol("sqrt()")),
                ("!", lambda: self.insert_symbol("!")),
                ("| |", lambda: self.insert_symbol("abs()")),
                ("∑", lambda: self.insert_symbol("Sum(, (, ))"))
            ]),
            ("Functions", [
                ("sin", lambda: self.insert_symbol("sin()")),
                ("cos", lambda: self.insert_symbol("cos()")),
                ("tan", lambda: self.insert_symbol("tan()")),
                ("log", lambda: self.insert_symbol("log()")),
                ("ln", lambda: self.insert_symbol("ln()")),
                ("exp", lambda: self.insert_symbol("exp()"))
            ]),
            ("Constants", [
                ("π", lambda: self.insert_symbol("pi")),
                ("e", lambda: self.insert_symbol("E")),
                ("∞", lambda: self.insert_symbol("oo")),
                ("i", lambda: self.insert_symbol("I"))
            ]),
            ("Greek", [
                ("α", lambda: self.insert_symbol("alpha")),
                ("β", lambda: self.insert_symbol("beta")),
                ("γ", lambda: self.insert_symbol("gamma")),
                ("θ", lambda: self.insert_symbol("theta"))
            ])
        ]
        
        for category, buttons in categories:
            cat_frame = ttk.LabelFrame(frame, text=category, padding=5)
            cat_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
            
            for text, command in buttons:
                btn = ttk.Button(cat_frame, text=text, command=command, width=6)
                btn.pack(side=tk.LEFT, padx=2, pady=2)

    def create_action_buttons(self):
        frame = ttk.Frame(self.top_panel)
        frame.pack(fill=tk.X, pady=10, padx=10)
        
        buttons = [
            ("Solve", self.on_solve_click, 'Accent.TButton'),
            ("Clear", self.clear_inputs, None),
            ("Copy Result", self.copy_result, None),
            ("Save Plot", self.save_plot, None),
            ("Export", self.export_result, None),
            ("Toggle Dark", self.toggle_dark_mode, None)
        ]
        
        for text, command, style in buttons:
            btn = ttk.Button(frame, text=text, command=command, style=style)
            btn.pack(side=tk.LEFT, expand=True, padx=5)

    def create_result_display(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.bottom_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10), padx=10)
        
        # Result tab
        self.result_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.result_frame, text="Result")
        
        self.result_text = tk.Text(self.result_frame, 
                                 wrap=tk.WORD, 
                                 font=('Consolas', 12),
                                 height=10,
                                 padx=10,
                                 pady=10)
        self.result_scroll = ttk.Scrollbar(self.result_frame, 
                                        command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=self.result_scroll.set)
        
        self.result_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Steps tab
        self.steps_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.steps_frame, text="Steps")
        
        self.steps_text = tk.Text(self.steps_frame, 
                                 wrap=tk.WORD, 
                                 font=('Consolas', 12),
                                 height=15,
                                 padx=10,
                                 pady=10)
        self.steps_scroll = ttk.Scrollbar(self.steps_frame, 
                                        command=self.steps_text.yview)
        self.steps_text.configure(yscrollcommand=self.steps_scroll.set)
        
        self.steps_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.steps_text.pack(fill=tk.BOTH, expand=True)
        
        # History tab
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="History")
        
        self.history_text = tk.Text(self.history_frame,
                                   wrap=tk.WORD,
                                   font=('Consolas', 11),
                                   height=10,
                                   padx=10,
                                   pady=10)
        self.history_scroll = ttk.Scrollbar(self.history_frame,
                                          command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=self.history_scroll.set)
        
        self.history_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Plot tab
        self.plot_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.plot_frame, text="Plot")
        
        # Add a clear history button
        history_btn_frame = ttk.Frame(self.history_frame)
        history_btn_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.clear_history_btn = ttk.Button(history_btn_frame, 
                                          text="Clear History", 
                                          command=self.clear_history)
        self.clear_history_btn.pack(side=tk.RIGHT)
        
        self.load_history_btn = ttk.Button(history_btn_frame,
                                         text="Load History",
                                         command=self.load_history)
        self.load_history_btn.pack(side=tk.RIGHT, padx=5)
        
        self.save_history_btn = ttk.Button(history_btn_frame,
                                         text="Save History",
                                         command=self.save_history)
        self.save_history_btn.pack(side=tk.RIGHT)

    def create_examples_section(self):
        frame = ttk.LabelFrame(self.top_panel, text="Examples", padding=10)
        frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Create notebook for example categories
        example_notebook = ttk.Notebook(frame)
        example_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Polynomial examples
        poly_frame = ttk.Frame(example_notebook)
        example_notebook.add(poly_frame, text="Polynomials")
        
        poly_examples = [
            ("Basic", "x**3 + 2*x**2 - 5*x + 7"),
            ("Multiple Variables", "x**2*y + x*y**2"),
            ("High Order", "x**5 - 3*x**3 + x")
        ]
        
        for name, expr in poly_examples:
            btn = ttk.Button(poly_frame, 
                           text=f"{name}: {expr}", 
                           command=lambda e=expr: self.insert_example(e))
            btn.pack(fill=tk.X, pady=2)
        
        # Trigonometric examples
        trig_frame = ttk.Frame(example_notebook)
        example_notebook.add(trig_frame, text="Trigonometric")
        
        trig_examples = [
            ("Basic", "sin(x)*cos(2*x)"),
            ("Composite", "tan(x**2 + 1)"),
            ("Inverse", "asin(x) + acos(x)")
        ]
        
        for name, expr in trig_examples:
            btn = ttk.Button(trig_frame, 
                           text=f"{name}: {expr}", 
                           command=lambda e=expr: self.insert_example(e))
            btn.pack(fill=tk.X, pady=2)
        
        # Exponential/Logarithmic examples
        exp_frame = ttk.Frame(example_notebook)
        example_notebook.add(exp_frame, text="Exponential/Log")
        
        exp_examples = [
            ("Exponential", "exp(-x**2)"),
            ("Logarithmic", "log(x**2 + 1)/x"),
            ("Natural Log", "ln(x) + ln(x+1)")
        ]
        
        for name, expr in exp_examples:
            btn = ttk.Button(exp_frame, 
                           text=f"{name}: {expr}", 
                           command=lambda e=expr: self.insert_example(e))
            btn.pack(fill=tk.X, pady=2)
        
        # Rational examples
        rat_frame = ttk.Frame(example_notebook)
        example_notebook.add(rat_frame, text="Rational")
        
        rat_examples = [
            ("Simple", "(3*x**2 + 2)/(x**3 + 2*x + 1)"),
            ("Partial Fractions", "1/(x**2 - 1)"),
            ("Complex", "(x**3 + x)/(x**4 + 1)")
        ]
        
        for name, expr in rat_examples:
            btn = ttk.Button(rat_frame, 
                           text=f"{name}: {expr}", 
                           command=lambda e=expr: self.insert_example(e))
            btn.pack(fill=tk.X, pady=2)
        
        # Equation solving examples
        eq_frame = ttk.Frame(example_notebook)
        example_notebook.add(eq_frame, text="Equations")
        
        eq_examples = [
            ("Linear", "2*x + 5 = 13"),
            ("Quadratic", "x**2 - 5*x + 6 = 0"),
            ("Trigonometric", "sin(x) = cos(x)")
        ]
        
        for name, expr in eq_examples:
            btn = ttk.Button(eq_frame, 
                           text=f"{name}: {expr}", 
                           command=lambda e=expr: self.insert_example(e))
            btn.pack(fill=tk.X, pady=2)

    def create_credits_section(self):
        """Create the credits section in the bottom panel"""
        frame = ttk.Frame(self.bottom_panel)
        frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        # Get versions with fallback
        def safe_get_version(module, attr='__version__'):
            try:
                version = getattr(module, attr)
                return f"{version:.2f}" if isinstance(version, float) else version
            except (AttributeError, TypeError):
                return "N/A"

        versions = {
            'SymPy': safe_get_version(sp),
            'Matplotlib': safe_get_version(matplotlib),
            'NumPy': safe_get_version(np),
            'Python': platform.python_version(),
            'Tk': safe_get_version(tk, 'TkVersion')
        }

        # Create version string
        version_text = " | ".join(f"{k} {v}" for k, v in versions.items())
        
        # Create and pack widgets
        credit_label = ttk.Label(
            frame,
            text=f"Developed by Manjil | {version_text}",
            font=('Arial', 8),
            foreground='#555555'
        )
        credit_label.pack(side=tk.LEFT, padx=(0, 10))

        btn_style = ttk.Style()
        btn_style.configure('Credit.TButton', font=('Arial', 8), padding=2)

        docs_btn = ttk.Button(
            frame,
            text="Docs",
            command=self.show_documentation,
            style='Credit.TButton',
            width=6
        )
        docs_btn.pack(side=tk.RIGHT)

        help_btn = ttk.Button(
            frame,
            text="Help",
            command=self.show_help,
            style='Credit.TButton',
            width=6
        )
        help_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
    def insert_symbol(self, symbol):
        """Insert a symbol at the current cursor position"""
        current_pos = self.entry_expression.index(tk.INSERT)
        self.entry_expression.insert(current_pos, symbol)
        
        # Move cursor inside parentheses if they were inserted
        if symbol.endswith("()"):
            new_pos = self.entry_expression.index(f"insert -{len(symbol)-1}c")
            self.entry_expression.icursor(new_pos)
    
    def insert_integration_symbol(self):
        if self.operation_var.get() == "Integral" and self.definite_var.get():
            self.insert_symbol("integrate(, , , )")
            pos = self.entry_expression.index(tk.INSERT)
            self.entry_expression.icursor(pos - 7)
        else:
            self.insert_symbol("integrate(, )")
            pos = self.entry_expression.index(tk.INSERT)
            self.entry_expression.icursor(pos - 3)
    
    def insert_derivative_symbol(self):
        self.insert_symbol("diff(, )")
        pos = self.entry_expression.index(tk.INSERT)
        self.entry_expression.icursor(pos - 3)
    
    def insert_power_operator(self):
        self.insert_symbol("**")
    
    def insert_example(self, example):
        self.entry_expression.delete(0, tk.END)
        self.entry_expression.insert(0, example)
        self.entry_variable.delete(0, tk.END)
        self.entry_variable.insert(0, "x")
        self.entry_expression.focus()

    def clear_inputs(self):
        self.entry_expression.delete(0, tk.END)
        self.entry_variable.delete(0, tk.END)
        self.entry_variable.insert(0, "x")
        self.order_var.set("1")
        self.definite_var.set(False)
        self.lower_limit_var.set("0")
        self.upper_limit_var.set("1")
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.steps_text.config(state=tk.NORMAL)
        self.steps_text.delete(1.0, tk.END)
        self.steps_text.config(state=tk.DISABLED)
        self.clear_plot()

    def clear_history(self):
        self.history = []
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        self.save_history()

    def save_history(self):
        try:
            with open('calc_history.pkl', 'wb') as f:
                pickle.dump(self.history, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save history: {e}")

    def load_history(self):
        try:
            if os.path.exists('calc_history.pkl'):
                with open('calc_history.pkl', 'rb') as f:
                    self.history = pickle.load(f)
                self.update_history_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load history: {e}")

    def update_history_display(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        if not self.history:
            self.history_text.insert(tk.END, "No history available")
        else:
            for i, item in enumerate(reversed(self.history), 1):
                self.history_text.insert(tk.END, f"{i}. {item['problem']}\n")
                self.history_text.insert(tk.END, f"   Result: {item['result']}\n\n")
        
        self.history_text.config(state=tk.DISABLED)

    def clear_plot(self):
        if self.plot_canvas:
            self.plot_canvas.get_tk_widget().destroy()
            self.plot_canvas = None
        if self.plot_img:
            self.plot_img = None

    def copy_result(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_text.get(1.0, tk.END))
        messagebox.showinfo("Copied", "Result copied to clipboard!")

    def save_plot(self):
        if not self.plot_canvas:
            messagebox.showerror("Error", "No plot available to save")
            return
        
        filetypes = [
            ('PNG Image', '*.png'),
            ('JPEG Image', '*.jpg'),
            ('PDF Document', '*.pdf'),
            ('SVG Vector', '*.svg')
        ]
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=filetypes,
            title="Save Plot As"
        )
        
        if filename:
            try:
                fig = self.plot_canvas.figure
                fig.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Success", f"Plot saved as {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save plot: {e}")

    def export_result(self):
        content = f"Problem: {self.current_problem}\n\n"
        content += "Result:\n" + self.result_text.get(1.0, tk.END) + "\n"
        content += "Steps:\n" + self.steps_text.get(1.0, tk.END)
        
        filetypes = [
            ('Text File', '*.txt'),
            ('LaTeX Document', '*.tex'),
            ('PDF Document', '*.pdf'),
            ('Markdown', '*.md')
        ]
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=filetypes,
            title="Export Result As"
        )
        
        if filename:
            try:
                if filename.endswith('.tex'):
                    self.export_latex(filename)
                elif filename.endswith('.pdf'):
                    self.export_pdf(filename)
                else:
                    with open(filename, 'w') as f:
                        f.write(content)
                messagebox.showinfo("Success", f"Result exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")

    def export_latex(self, filename):
        problem = self.current_problem
        result = self.result_text.get(1.0, tk.END)
        steps = self.steps_text.get(1.0, tk.END)
        
        latex_content = r"""\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\begin{document}

\section*{Problem}
\[ """ + latex(expression = expression.replace('^', '**'))
parse_expr(problem.split('=')[0] if '=' in problem else problem) + r""" \]

\section*{Result}
\[ """ + latex(expression = expression.replace('^', '**'))
parse_expr(result.split('=')[1] if '=' in result else result) + r""" \]

\section*{Solution Steps}
\begin{itemize}
""" + "\n".join([r"    \item " + step for step in steps.split('\n') if step.strip()]) + r"""
\end{itemize}

\end{document}"""
        
with open(filename, 'w') as f:
            f.write(latex_content)

    def export_pdf(self, filename):
        from fpdf import FPDF
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="Problem:", ln=1)
        pdf.multi_cell(0, 10, txt=self.current_problem)
        
        pdf.cell(200, 10, txt="Result:", ln=1)
        pdf.multi_cell(0, 10, txt=self.result_text.get(1.0, tk.END))
        
        pdf.cell(200, 10, txt="Steps:", ln=1)
        pdf.multi_cell(0, 10, txt=self.steps_text.get(1.0, tk.END))
        
        pdf.output(filename)

    def toggle_dark_mode(self):
        self.dark_mode_var.set(not self.dark_mode_var.get())
        
        if self.dark_mode_var.get():
            # Dark mode colors
            bg = '#2d2d2d'
            fg = '#ffffff'
            entry_bg = '#3d3d3d'
            self.style.configure('.', background=bg, foreground=fg)
            self.style.configure('TFrame', background=bg)
            self.style.configure('TLabel', background=bg, foreground=fg)
            self.style.configure('TEntry', fieldbackground=entry_bg, foreground=fg)
            self.style.configure('TText', background=entry_bg, foreground=fg)
            self.style.configure('TCombobox', fieldbackground=entry_bg, foreground=fg)
        else:
            # Light mode colors
            bg = '#f0f0f0'
            fg = '#000000'
            entry_bg = '#ffffff'
            self.style.configure('.', background=bg, foreground=fg)
            self.style.configure('TFrame', background=bg)
            self.style.configure('TLabel', background=bg, foreground=fg)
            self.style.configure('TEntry', fieldbackground=entry_bg, foreground=fg)
            self.style.configure('TText', background=entry_bg, foreground=fg)
            self.style.configure('TCombobox', fieldbackground=entry_bg, foreground=fg)

    def validate_inputs(self):
        expression = self.entry_expression.get()
        variable = self.entry_variable.get()
        operation = self.operation_var.get()
        
        if not expression:
            messagebox.showerror("Input Error", "Please enter a mathematical expression.")
            return False
        
        if not variable:
            messagebox.showerror("Input Error", "Please specify a variable.")
            return False
        
        if not re.match(r'^[a-zA-Z]$', variable):
            messagebox.showerror("Input Error", "Variable must be a single letter.")
            return False
        
        if operation == "Derivative":
            try:
                order = int(self.order_var.get())
                if order <= 0:
                    messagebox.showerror("Input Error", "Derivative order must be positive.")
                    return False
            except ValueError:
                messagebox.showerror("Input Error", "Derivative order must be an integer.")
                return False
        
        if operation == "Integral" and self.definite_var.get():
            try:
                float(self.lower_limit_var.get())
                float(self.upper_limit_var.get())
            except ValueError:
                messagebox.showerror("Input Error", "Integration limits must be numbers.")
                return False
        
        if operation in ["Limit", "Series"]:
            try:
                float(self.order_var.get())
            except ValueError:
                messagebox.showerror("Input Error", "Point/Order must be a number.")
                return False
        
        return True

    def solve_derivative(self, expression, variable, order):
        try:
            x = sp.symbols(variable)
            expr = expression = expression.replace('^', '**')
parse_expr(expression, transformations=self.transformations)
            
                        # Check if variable exists in expression
            if x not in expr.free_symbols:
                return f"Expression does not contain the variable {variable}", ""
            
            derivative = sp.diff(expr, x, order)
            
            # Create step-by-step explanation
            steps = f"Step 1: Original function: {sp.pretty(expr)}\n\n"
            steps += f"Step 2: Compute derivative with respect to {variable}"
            if order > 1:
                steps += f" (order {order})"
            steps += ":\n"
            
            if order == 1:
                steps += f"d/d{variable} [{sp.pretty(expr)}] = {sp.pretty(derivative)}\n"
            else:
                steps += f"d^{order}/d{variable}^{order} [{sp.pretty(expr)}] = {sp.pretty(derivative)}\n"
            
            steps += "\nStep 3: Final result:"
            
            return f"d^{order}/d{variable}^{order} [{sp.pretty(expr)}] = {sp.pretty(derivative)}", steps
        zexcept Exception as e:
            return f"Error calculating derivative: {str(e)}", ""

    def solve_integral(self, expression, variable, definite, lower, upper):
     try:
        # Clean and validate the input expression
        clean_expr = expression.strip()
        
        # Handle empty input
        if not clean_expr:
            return "Error: Please enter an expression to integrate", ""
            
        # Remove 'integrate(' and ')' if present
        if clean_expr.startswith('integrate(') and clean_expr.endswith(')'):
            clean_expr = clean_expr[9:-1]  # Remove 'integrate(' and ')'
        
        # Split into components if comma exists
        parts = [part.strip() for part in clean_expr.split(',') if part.strip()]
        
        # Get the main expression part (first part before comma)
        if not parts:
            return "Error: No expression found", ""
            
        main_expr = parts[0]
        
        # Parse the expression
        try:
            x = sp.symbols(variable)
            expr = expression = expression.replace('^', '**')
parse_expr(main_expr, transformations=self.transformations)
        except Exception as e:
            return f"Error parsing expression: {str(e)}", ""
        
        # Verify the variable exists in the expression
        if x not in expr.free_symbols:
            return f"Error: Expression doesn't contain the variable '{variable}'", ""
        
        # Prepare steps explanation
        steps = f"Step 1: Original function: {sp.pretty(expr)}\n\n"
        
        # Compute the integral
        if definite:
            try:
                lower_val = sp.sympify(lower)
                upper_val = sp.sympify(upper)
                integral = sp.integrate(expr, (x, lower_val, upper_val))
                result = f"Definite integral from {lower} to {upper}:\n"
                result += f"∫[{lower} to {upper}] {sp.pretty(expr)} d{variable} = {sp.pretty(integral)}"
                steps += f"Step 2: Computed definite integral:\n{result}\n"
            except Exception as e:
                return f"Error computing definite integral: {str(e)}", ""
        else:
            try:
                integral = sp.integrate(expr, x)
                if isinstance(integral, sp.Integral):
                    result = f"Integral could not be computed symbolically:\n"
                    result += f"∫ {sp.pretty(expr)} d{variable} = {sp.pretty(integral)}"
                    steps += "Step 2: Could not find symbolic solution\n"
                else:
                    result = f"Indefinite integral:\n"
                    result += f"∫ {sp.pretty(expr)} d{variable} = {sp.pretty(integral)} + C"
                    steps += f"Step 2: Computed indefinite integral:\n{result}\n"
            except Exception as e:
                return f"Error computing indefinite integral: {str(e)}", ""
        
        steps += "\nStep 3: Final result"
        return result, steps
        
     except Exception as e:
        return f"Unexpected error: {str(e)}", ""

    def solve_equation(self, expression, variable):
         try:
            x = sp.symbols(variable)
            
            # Handle both "expr = 0" and "expr1 = expr2" formats
            if '=' in expression:
                parts = expression.split('=')
                lhs = expression = expression.replace('^', '**')
parse_expr(parts[0].strip(), transformations=self.transformations)
                rhs = expression = expression.replace('^', '**')
parse_expr(parts[1].strip(), transformations=self.transformations)
                equation = sp.Eq(lhs, rhs)
            else:
                expr = expression = expression.replace('^', '**')
parse_expr(expression, transformations=self.transformations)
                equation = sp.Eq(expr, 0)
            
            # Check if variable exists in equation
            if x not in equation.free_symbols:
                return f"Equation does not contain the variable {variable}", ""
            
            solutions = sp.solveset(equation, x)
            
            steps = f"Step 1: Original equation: {sp.pretty(equation)}\n\n"
            steps += "Step 2: Solving for {}:\n".format(variable)
            
            if isinstance(solutions, sp.FiniteSet):
                steps += "Solutions:\n"
                for sol in solutions:
                    steps += f"{variable} = {sp.pretty(sol)}\n"
                result = f"Solutions to {sp.pretty(equation)}:\n"
                result += "\n".join([f"{variable} = {sp.pretty(sol)}" for sol in solutions])
            else:
                steps += f"Solution set: {sp.pretty(solutions)}\n"
                result = f"Solution set for {sp.pretty(equation)}: {sp.pretty(solutions)}"
            
            steps += "\nStep 3: Final result:"
            
            return result, steps
         except Exception as e:
            return f"Error solving equation: {str(e)}", ""
    def solve_limit(self, expression, variable, point):
         try:
            x = sp.symbols(variable)
            expr = expression = expression.replace('^', '**')
parse_expr(expression, transformations=self.transformations)
            
            # Check if variable exists in expression
            if x not in expr.free_symbols:
                return f"Expression does not contain the variable {variable}", ""
            
            point_expr = expression = expression.replace('^', '**')
parse_expr(point, transformations=self.transformations)
            lim = limit(expr, x, point_expr)
            
            steps = f"Step 1: Original function: {sp.pretty(expr)}\n\n"
            steps += f"Step 2: Compute limit as {variable} approaches {point}:\n"
            steps += f"lim({sp.pretty(expr)}) as {variable}->{point} = {sp.pretty(lim)}\n"
            steps += "\nStep 3: Final result:"
            
            return f"lim({sp.pretty(expr)}) as {variable}->{point} = {sp.pretty(lim)}", steps
         except Exception as e:
            return f"Error calculating limit: {str(e)}", ""

    def solve_series(self, expression, variable, order):
        try:
            x = sp.symbols(variable)
            expr = expression = expression.replace('^', '**')
parse_expr(expression, transformations=self.transformations)
            
            # Check if variable exists in expression
            if x not in expr.free_symbols:
                return f"Expression does not contain the variable {variable}", ""
            
            try:
                order_int = int(order)
            except ValueError:
                return "Series order must be an integer", ""
            
            ser = series(expr, x, n=order_int)
            
            steps = f"Step 1: Original function: {sp.pretty(expr)}\n\n"
            steps += f"Step 2: Compute series expansion to order {order}:\n"
            steps += f"Series expansion of {sp.pretty(expr)} at {variable}=0:\n{sp.pretty(ser)}\n"
            steps += "\nStep 3: Final result:"
            
            return f"Series expansion of {sp.pretty(expr)} at {variable}=0:\n{sp.pretty(ser)}", steps
        except Exception as e:
            return f"Error calculating series expansion: {str(e)}", ""

    def generate_plot(self, expression, variable, result_expr=None):
        try:
            x = sp.symbols(variable)
            expr = expression = expression.replace('^', '**')
parse_expr(expression, transformations=self.transformations)
            
            # Clear previous plot
            self.clear_plot()
            
            # Determine plot range
            if self.plot_range_var.get() == "Auto":
                x_min, x_max = -5, 5
            else:
                x_min = float(self.custom_min_var.get())
                x_max = float(self.custom_max_var.get())
            
            # Create plot
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Convert sympy expression to numpy function
            f = sp.lambdify(x, expr, 'numpy')
            x_vals = np.linspace(x_min, x_max, 400)
            y_vals = f(x_vals)
            
            # Plot original function
            ax.plot(x_vals, y_vals, label=f'${sp.latex(expr)}$', linewidth=2)
            
            # Plot result if it's a function
            if result_expr:
                try:
                    result_expr = expression = expression.replace('^', '**')
parse_expr(result_expr.split('=')[1].split('+')[0].strip(), transformations=self.transformations)
                    f_result = sp.lambdify(x, result_expr, 'numpy')
                    y_result = f_result(x_vals)
                    ax.plot(x_vals, y_result, '--', label=f'${sp.latex(result_expr)}$', linewidth=2)
                except:
                    pass
            
            # Add labels and legend
            ax.set_xlabel(variable, fontsize=12)
            ax.set_ylabel(f'f({variable})', fontsize=12)
            ax.set_title(f'Plot of {sp.pretty(expr)}', fontsize=14)
            ax.legend(fontsize=10)
            ax.grid(True)
            
            # Adjust layout
            fig.tight_layout()
            
            # Embed plot in Tkinter
            self.plot_canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            self.plot_canvas.draw()
            self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add toolbar
            toolbar = NavigationToolbar2Tk(self.plot_canvas, self.plot_frame)
            toolbar.update()
            self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Plot Error", f"Failed to generate plot: {str(e)}")

    def on_solve_click(self, event=None):
        if not self.validate_inputs():
            return
        
        # Get inputs
        expression = self.entry_expression.get()
        variable = self.entry_variable.get()
        operation = self.operation_var.get()
        
        # Create problem description
        self.current_problem = f"{operation} of {expression} with respect to {variable}"
        if operation == "Derivative":
            self.current_problem += f" (order {self.order_var.get()})"
        elif operation == "Integral" and self.definite_var.get():
            self.current_problem += f" from {self.lower_limit_var.get()} to {self.upper_limit_var.get()}"
        elif operation in ["Limit", "Series"]:
            self.current_problem += f" at {self.order_var.get()}"
        
        # Solve in a separate thread to prevent UI freezing
        threading.Thread(target=self.solve_in_thread, daemon=True).start()

    def solve_in_thread(self):
        try:
            expression = self.entry_expression.get()
            variable = self.entry_variable.get()
            operation = self.operation_var.get()
            
            result = ""
            steps = ""
            result_expr = ""
            
            if operation == "Derivative":
                order = int(self.order_var.get())
                result, steps = self.solve_derivative(expression, variable, order)
                result_expr = result.split('=')[1].strip()
            elif operation == "Integral":
                definite = self.definite_var.get()
                lower = self.lower_limit_var.get()
                upper = self.upper_limit_var.get()
                result, steps = self.solve_integral(expression, variable, definite, lower, upper)
                result_expr = result.split('=')[0].split('∫')[1].strip()
            elif operation == "Limit":
                point = self.order_var.get()
                result, steps = self.solve_limit(expression, variable, point)
            elif operation == "Series":
                order = self.order_var.get()
                result, steps = self.solve_series(expression, variable, order)
            elif operation == "Solve":
                result, steps = self.solve_equation(expression, variable)
            
            # Add to history
            self.history.append({
                'problem': self.current_problem,
                'result': result.split('\n')[0][:50] + "..." if len(result) > 50 else result
            })
            if len(self.history) > 50:  # Limit history size
                self.history.pop(0)
            
            # Placeholder for LaTeX preview (TODO: implement image generation for rendered LaTeX)
            self.result_queue.put({
                'result': result,
                'steps': steps,
                'result_expr': result_expr if 'result_expr' in locals() else None
            })
            
        except Exception as e:
            self.result_queue.put({
                'result': f"Error: {str(e)}",
                'steps': "",
                'result_expr': None
            })

    def process_result_queue(self):
        try:
            while not self.result_queue.empty():
                result_data = self.result_queue.get()
                
                # Update result display
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, result_data['result'])
                self.result_text.config(state=tk.DISABLED)
                
                # Update steps display
                self.steps_text.config(state=tk.NORMAL)
                self.steps_text.delete(1.0, tk.END)
                self.steps_text.after(0, self.animate_steps, result_data['steps'].split('\n'))
                # Skip direct insert to allow animation
                self.steps_text.config(state=tk.DISABLED)
                
                # Generate plot if applicable
                if result_data['result_expr'] and self.operation_var.get() in ["Derivative", "Integral"]:
                    self.generate_plot(self.entry_expression.get(), 
                                     self.entry_variable.get(),
                                     result_data['result_expr'])
                
                # Update history
                self.update_history_display()
                self.save_history()
                
        finally:
            # Check again after 100ms
            self.root.after(100, self.process_result_queue)

    def show_documentation(self):
        docs_url = "https://docs.sympy.org/latest/index.html"
        webbrowser.open_new_tab(docs_url)

    def animate_steps(self, steps_list):
        self.steps_text.delete(1.0, tk.END)
        def add_line(i=0):
            if i < len(steps_list):
                self.steps_text.insert(tk.END, steps_list[i] + '\n')
                self.steps_text.see(tk.END)
                self.steps_text.after(150, add_line, i + 1)
        add_line()

    def show_help(self):
        help_text = """Advanced Calculus Solver Pro - Help

1. Enter a mathematical expression in the input field.
2. Select the operation you want to perform.
3. Specify any additional parameters (order, limits, etc.).
4. Click 'Solve' to compute the result.

Examples:
- Derivative: x**2 + 3*x - 5
- Integral: sin(x)*cos(x)
- Limit: (sin(x)/x)
- Series: exp(x)
- Solve: x**2 - 4 = 0

Use the symbol buttons to help with input.
Results can be copied, saved, or exported.
"""
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedMathSolver(root)
    root.mainloop()

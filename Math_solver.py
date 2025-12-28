"""
Advanced Calculus Solver Pro - Version 2.0 Enhanced Edition
A professional mathematical computation tool for calculus operations.
Features: 9+ operations, step-by-step solutions, plotting, export, history
Created: December 28, 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import tkinter.font as tkFont
import sympy as sp
from sympy import (
    symbols, diff, integrate, limit, series, solve, simplify, 
    factor, expand, apart, Symbol, sympify, lambdify,
    sin, cos, tan, cot, sec, csc, sinh, cosh, tanh,
    asin, acos, atan, asinh, acosh, atanh,
    exp, log, ln, sqrt, cbrt, Abs, sign, ceil, floor,
    factorial, gamma, zeta, pi, E, I, oo, nan, zoo,
    Rational, Poly, roots, Eq, re, im, conjugate,
    Array, Matrix, eye, zeros, ones, diag
)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import traceback
from datetime import datetime
import json
import os
from PIL import Image, ImageDraw, ImageFont
import io
from scipy import optimize, integrate as scipy_integrate, special
import webbrowser


class MathExpressionParser:
    """Advanced expression parser with error handling"""

    def __init__(self):
        """Initialize parser with all symbols"""
        self.x = symbols('x')
        self.y = symbols('y')
        self.z = symbols('z')
        self.t = symbols('t')
        self.n = symbols('n', integer=True)
        self.transformations = (standard_transformations + (implicit_multiplication_application,))

    def parse(self, expression_str):
        """Parse mathematical expression string"""
        try:
            expr_str = expression_str.replace('^', '**')
            expr_str = expr_str.replace('−', '-')  # Handle special minus

            # Create local namespace
            local_dict = {
                'x': self.x, 'y': self.y, 'z': self.z, 't': self.t, 'n': self.n,
                'sin': sin, 'cos': cos, 'tan': tan, 'cot': cot, 'sec': sec, 'csc': csc,
                'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
                'asin': asin, 'acos': acos, 'atan': atan,
                'asinh': asinh, 'acosh': acosh, 'atanh': atanh,
                'exp': exp, 'log': log, 'ln': ln, 'sqrt': sqrt, 'cbrt': cbrt,
                'Abs': Abs, 'sign': sign, 'ceil': ceil, 'floor': floor,
                'factorial': factorial, 'gamma': gamma, 'zeta': zeta,
                'pi': pi, 'e': E, 'E': E, 'i': I, 'I': I,
                'oo': oo, 'inf': oo, 'infinity': oo,
                'conjugate': conjugate, 're': re, 'im': im,
            }

            expr = parse_expr(expr_str, transformations=self.transformations, local_dict=local_dict)
            return expr
        except Exception as e:
            raise ValueError(f"Parse error: {str(e)}")


class CalcutusSolver:
    """Core mathematical solver engine"""

    def __init__(self):
        """Initialize solver"""
        self.parser = MathExpressionParser()
        self.x = symbols('x')
        self.y = symbols('y')
        self.z = symbols('z')

    def derivative(self, expr, order=1):
        """Calculate derivative"""
        try:
            result = diff(expr, self.x, order)
            steps = [
                f"Expression: {expr}",
                f"Variable: x",
                f"Order: {order}",
                f"Applying differentiation rules...",
                f"Result: {result}"
            ]
            return result, steps
        except Exception as e:
            raise ValueError(f"Derivative error: {str(e)}")

    def integral(self, expr, limit_lower=None, limit_upper=None):
        """Calculate indefinite or definite integral"""
        try:
            if limit_lower is None or limit_upper is None:
                result = integrate(expr, self.x)
                steps = [
                    f"Expression: {expr}",
                    f"Variable: x",
                    f"Computing indefinite integral...",
                    f"Result: {result} + C"
                ]
            else:
                result = integrate(expr, (self.x, limit_lower, limit_upper))
                steps = [
                    f"Expression: {expr}",
                    f"Limits: x from {limit_lower} to {limit_upper}",
                    f"Computing definite integral...",
                    f"Result: {result}"
                ]
            return result, steps
        except Exception as e:
            raise ValueError(f"Integral error: {str(e)}")

    def limit_calc(self, expr, point=0, direction='+'):
        """Calculate limit"""
        try:
            if direction == '+':
                result = limit(expr, self.x, point, '+')
            elif direction == '-':
                result = limit(expr, self.x, point, '-')
            else:
                result = limit(expr, self.x, point)

            steps = [
                f"Expression: {expr}",
                f"Point: {point}",
                f"Direction: {direction if direction in ['+', '-'] else 'both'}",
                f"Computing limit...",
                f"Result: {result}"
            ]
            return result, steps
        except Exception as e:
            raise ValueError(f"Limit error: {str(e)}")

    def series_expansion(self, expr, point=0, order=6):
        """Taylor/Maclaurin series expansion"""
        try:
            result = series(expr, self.x, point, n=order)
            steps = [
                f"Expression: {expr}",
                f"Point: {point}",
                f"Order: {order}",
                f"Computing Taylor series...",
                f"Result: {result}"
            ]
            return result, steps
        except Exception as e:
            raise ValueError(f"Series error: {str(e)}")

    def solve_equation(self, expr):
        """Solve equation (expr = 0)"""
        try:
            solutions = solve(expr, self.x)
            if not solutions:
                solutions = ["No solutions found"]

            steps = [
                f"Equation: {expr} = 0",
                f"Variable: x",
                f"Solving algebraically...",
                f"Solutions: {solutions}"
            ]
            return solutions, steps
        except Exception as e:
            raise ValueError(f"Solve error: {str(e)}")

    def simplify_expr(self, expr):
        """Simplify expression"""
        try:
            result = simplify(expr)
            steps = [
                f"Expression: {expr}",
                f"Applying simplification rules...",
                f"Result: {result}"
            ]
            return result, steps
        except Exception as e:
            raise ValueError(f"Simplify error: {str(e)}")

    def factor_expr(self, expr):
        """Factor polynomial"""
        try:
            result = factor(expr)
            steps = [
                f"Expression: {expr}",
                f"Factoring polynomial...",
                f"Result: {result}"
            ]
            return result, steps
        except Exception as e:
            raise ValueError(f"Factor error: {str(e)}")

    def expand_expr(self, expr):
        """Expand expression"""
        try:
            result = expand(expr)
            steps = [
                f"Expression: {expr}",
                f"Expanding all terms...",
                f"Result: {result}"
            ]
            return result, steps
        except Exception as e:
            raise ValueError(f"Expand error: {str(e)}")

    def partial_fractions(self, expr):
        """Partial fraction decomposition"""
        try:
            result = apart(expr, self.x)
            steps = [
                f"Expression: {expr}",
                f"Decomposing into partial fractions...",
                f"Result: {result}"
            ]
            return result, steps
        except Exception as e:
            raise ValueError(f"Partial fractions error: {str(e)}")

    def second_derivative(self, expr):
        """Calculate second derivative"""
        return self.derivative(expr, order=2)

    def third_derivative(self, expr):
        """Calculate third derivative"""
        return self.derivative(expr, order=3)

    def critical_points(self, expr):
        """Find critical points (where derivative = 0)"""
        try:
            first_deriv = diff(expr, self.x)
            critical = solve(first_deriv, self.x)
            steps = [
                f"Expression: {expr}",
                f"First derivative: {first_deriv}",
                f"Setting derivative = 0...",
                f"Critical points: {critical}"
            ]
            return critical, steps
        except Exception as e:
            raise ValueError(f"Critical points error: {str(e)}")

    def inflection_points(self, expr):
        """Find inflection points (where second derivative = 0)"""
        try:
            second_deriv = diff(expr, self.x, 2)
            inflection = solve(second_deriv, self.x)
            steps = [
                f"Expression: {expr}",
                f"Second derivative: {second_deriv}",
                f"Setting second derivative = 0...",
                f"Inflection points: {inflection}"
            ]
            return inflection, steps
        except Exception as e:
            raise ValueError(f"Inflection points error: {str(e)}")


class GraphPlotter:
    """Advanced function plotting with matplotlib"""

    def __init__(self):
        """Initialize plotter"""
        self.x = symbols('x')

    def plot_function(self, expr, x_min=-10, x_max=10, resolution=1000):
        """Plot function"""
        try:
            # Convert to callable function
            f = lambdify(self.x, expr, 'numpy')

            # Create x values
            x_vals = np.linspace(x_min, x_max, resolution)

            # Calculate y values with error handling
            y_vals = []
            for x_val in x_vals:
                try:
                    y = f(x_val)
                    if isinstance(y, complex):
                        y = np.abs(y)
                    if np.isfinite(y):
                        y_vals.append(y)
                    else:
                        y_vals.append(np.nan)
                except:
                    y_vals.append(np.nan)

            y_vals = np.array(y_vals)

            # Create figure
            fig = Figure(figsize=(8, 5), dpi=100)
            ax = fig.add_subplot(111)

            # Plot
            ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=str(expr))
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('x', fontsize=12)
            ax.set_ylabel('y', fontsize=12)
            ax.set_title(f'Graph of {expr}', fontsize=14, fontweight='bold')
            ax.legend()

            # Set reasonable y limits
            y_filtered = y_vals[np.isfinite(y_vals)]
            if len(y_filtered) > 0:
                y_min, y_max = np.min(y_filtered), np.max(y_filtered)
                y_range = y_max - y_min
                if y_range == 0:
                    y_range = 1
                ax.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)

            return fig
        except Exception as e:
            raise ValueError(f"Plot error: {str(e)}")

    def plot_derivative(self, expr, x_min=-10, x_max=10):
        """Plot function and its derivative"""
        try:
            deriv = diff(expr, self.x)
            f = lambdify(self.x, expr, 'numpy')
            f_prime = lambdify(self.x, deriv, 'numpy')

            x_vals = np.linspace(x_min, x_max, 1000)
            y_vals = []
            y_prime_vals = []

            for x_val in x_vals:
                try:
                    y = f(x_val)
                    if isinstance(y, complex):
                        y = np.abs(y)
                    y_vals.append(y if np.isfinite(y) else np.nan)

                    y_p = f_prime(x_val)
                    if isinstance(y_p, complex):
                        y_p = np.abs(y_p)
                    y_prime_vals.append(y_p if np.isfinite(y_p) else np.nan)
                except:
                    y_vals.append(np.nan)
                    y_prime_vals.append(np.nan)

            y_vals = np.array(y_vals)
            y_prime_vals = np.array(y_prime_vals)

            fig = Figure(figsize=(10, 6), dpi=100)

            ax1 = fig.add_subplot(121)
            ax1.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
            ax1.grid(True, alpha=0.3)
            ax1.set_xlabel('x', fontsize=10)
            ax1.set_ylabel('y', fontsize=10)
            ax1.set_title(f'f(x) = {expr}', fontsize=12)
            ax1.legend()

            ax2 = fig.add_subplot(122)
            ax2.plot(x_vals, y_prime_vals, 'r-', linewidth=2, label="f'(x)")
            ax2.grid(True, alpha=0.3)
            ax2.set_xlabel('x', fontsize=10)
            ax2.set_ylabel("y'", fontsize=10)
            ax2.set_title(f"f'(x) = {deriv}", fontsize=12)
            ax2.legend()

            fig.tight_layout()
            return fig
        except Exception as e:
            raise ValueError(f"Derivative plot error: {str(e)}")


class EnhancedMathSolver:
    """Main GUI application"""

    def __init__(self, root):
        """Initialize application"""
        self.root = root
        self.root.title("Advanced Calculus Solver Pro - Version 2.0")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)

        # Initialize solvers
        self.solver = CalcutusSolver()
        self.plotter = GraphPlotter()
        self.x = symbols('x')

        # Variables
        self.expression_var = tk.StringVar()
        self.operation_var = tk.StringVar(value="Derivative")
        self.history = []
        self.current_result = None
        self.current_steps = []
        self.current_expr = None

        # Setup UI
        self.setup_styles()
        self.create_widgets()
        self.bind_shortcuts()
        self.load_history()

    def setup_styles(self):
        """Setup application styles"""
        style = ttk.Style()
        style.theme_use('clam')

        self.bg_color = "#f5f5f5"
        self.header_color = "#1e3a8a"
        self.button_color = "#2563eb"
        self.button_hover = "#1d4ed8"
        self.text_color = "#1f2937"
        self.highlight_color = "#dbeafe"

        self.root.configure(bg=self.bg_color)

    def create_widgets(self):
        """Create all UI widgets"""
        # Header
        self.create_header()

        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel (Input & Controls)
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))

        self.create_input_section(left_panel)
        self.create_buttons_section(left_panel)

        # Right panel (Results)
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_results_section(right_panel)

    def create_header(self):
        """Create application header"""
        header = tk.Frame(self.root, bg=self.header_color, height=80)
        header.pack(fill=tk.X)

        # Title
        title_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
        title = tk.Label(
            header,
            text="Advanced Calculus Solver Pro v2.0",
            font=title_font,
            bg=self.header_color,
            fg="white"
        )
        title.pack(pady=10)

        # Subtitle
        subtitle = tk.Label(
            header,
            text="Professional Mathematical Computation Tool | Derivatives • Integrals • Limits • Series • Solutions",
            font=("Helvetica", 10),
            bg=self.header_color,
            fg="#e0e7ff"
        )
        subtitle.pack()

    def create_input_section(self, parent):
        """Create input section"""
        input_frame = ttk.LabelFrame(parent, text="Input Expression", padding=12)
        input_frame.pack(fill=tk.X, pady=10)

        # Expression
        expr_label = ttk.Label(input_frame, text="Expression:", font=("Helvetica", 10))
        expr_label.pack(anchor=tk.W, pady=(0, 5))

        expr_entry = ttk.Entry(
            input_frame,
            textvariable=self.expression_var,
            font=("Courier", 11),
            width=35
        )
        expr_entry.pack(fill=tk.X, pady=(0, 10))
        expr_entry.bind("<Return>", lambda e: self.solve())

        # Operation
        op_label = ttk.Label(input_frame, text="Operation:", font=("Helvetica", 10))
        op_label.pack(anchor=tk.W, pady=(0, 5))

        operations = [
            "Derivative",
            "2nd Derivative",
            "3rd Derivative",
            "Integral (Indefinite)",
            "Integral (Definite)",
            "Limit",
            "Series Expansion",
            "Solve Equation",
            "Critical Points",
            "Inflection Points",
            "Simplify",
            "Factor",
            "Expand",
            "Partial Fractions"
        ]

        op_combo = ttk.Combobox(
            input_frame,
            textvariable=self.operation_var,
            values=operations,
            state="readonly",
            width=32,
            font=("Helvetica", 10)
        )
        op_combo.pack(fill=tk.X)

    def create_buttons_section(self, parent):
        """Create buttons section"""
        button_frame = ttk.LabelFrame(parent, text="Controls", padding=10)
        button_frame.pack(fill=tk.X, pady=10)

        # Solve button (main)
        solve_btn = tk.Button(
            button_frame,
            text="✓ SOLVE",
            command=self.solve,
            bg=self.button_color,
            fg="white",
            font=("Helvetica", 12, "bold"),
            padx=15,
            pady=10,
            relief=tk.RAISED,
            bd=2
        )
        solve_btn.pack(fill=tk.X, pady=5)

        # Action buttons
        actions_frame = ttk.Frame(button_frame)
        actions_frame.pack(fill=tk.X, pady=5)

        clear_btn = tk.Button(
            actions_frame,
            text="Clear",
            command=self.clear,
            bg="#6b7280",
            fg="white",
            font=("Helvetica", 10),
            padx=10,
            pady=8,
            relief=tk.FLAT
        )
        clear_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        copy_btn = tk.Button(
            actions_frame,
            text="Copy",
            command=self.copy_result,
            bg="#6b7280",
            fg="white",
            font=("Helvetica", 10),
            padx=10,
            pady=8,
            relief=tk.FLAT
        )
        copy_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        export_btn = tk.Button(
            actions_frame,
            text="Export",
            command=self.export_result,
            bg="#6b7280",
            fg="white",
            font=("Helvetica", 10),
            padx=10,
            pady=8,
            relief=tk.FLAT
        )
        export_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        # Help and Info
        help_frame = ttk.Frame(button_frame)
        help_frame.pack(fill=tk.X, pady=5)

        help_btn = tk.Button(
            help_frame,
            text="Help",
            command=self.show_help,
            bg="#8b5cf6",
            fg="white",
            font=("Helvetica", 10),
            padx=10,
            pady=8,
            relief=tk.FLAT
        )
        help_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        syntax_btn = tk.Button(
            help_frame,
            text="Syntax",
            command=self.show_syntax,
            bg="#8b5cf6",
            fg="white",
            font=("Helvetica", 10),
            padx=10,
            pady=8,
            relief=tk.FLAT
        )
        syntax_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        # Examples section
        examples_frame = ttk.LabelFrame(parent, text="Quick Examples", padding=10)
        examples_frame.pack(fill=tk.X, pady=10)

        examples = [
            ("x**2", "Basic"),
            ("sin(x)", "Trig"),
            ("exp(x)", "Exp"),
            ("1/(x-1)", "Rational"),
        ]

        for i, (expr, label) in enumerate(examples):
            btn = tk.Button(
                examples_frame,
                text=label,
                command=lambda e=expr: self.expression_var.set(e),
                bg="#e5e7eb",
                fg=self.text_color,
                font=("Helvetica", 9),
                relief=tk.FLAT,
                padx=8,
                pady=5
            )
            btn.pack(fill=tk.X, pady=2)

    def create_results_section(self, parent):
        """Create results section with tabs"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Result tab
        result_frame = ttk.Frame(self.notebook)
        self.notebook.add(result_frame, text="📊 Result")

        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=15,
            font=("Courier", 11),
            bg="white",
            fg=self.text_color,
            padx=10,
            pady=10
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Steps tab
        steps_frame = ttk.Frame(self.notebook)
        self.notebook.add(steps_frame, text="📝 Steps")

        self.steps_text = scrolledtext.ScrolledText(
            steps_frame,
            height=15,
            font=("Courier", 10),
            bg="white",
            fg=self.text_color,
            padx=10,
            pady=10
        )
        self.steps_text.pack(fill=tk.BOTH, expand=True)

        # History tab
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="📜 History")

        history_controls = ttk.Frame(history_frame)
        history_controls.pack(fill=tk.X, padx=5, pady=5)

        clear_history_btn = tk.Button(
            history_controls,
            text="Clear History",
            command=self.clear_history,
            bg="#ef4444",
            fg="white",
            font=("Helvetica", 9),
            padx=10,
            pady=5,
            relief=tk.FLAT
        )
        clear_history_btn.pack(side=tk.RIGHT)

        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            height=14,
            font=("Courier", 9),
            bg="white",
            fg=self.text_color,
            padx=10,
            pady=10
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)

        # Plot tab
        plot_frame = ttk.Frame(self.notebook)
        self.notebook.add(plot_frame, text="📈 Plot")

        plot_controls = ttk.Frame(plot_frame)
        plot_controls.pack(fill=tk.X, padx=5, pady=5)

        plot_btn = tk.Button(
            plot_controls,
            text="Plot Function",
            command=self.plot_function,
            bg="#10b981",
            fg="white",
            font=("Helvetica", 10),
            padx=15,
            pady=5,
            relief=tk.FLAT
        )
        plot_btn.pack(side=tk.LEFT, padx=5)

        plot_deriv_btn = tk.Button(
            plot_controls,
            text="Plot with Derivative",
            command=self.plot_derivative,
            bg="#10b981",
            fg="white",
            font=("Helvetica", 10),
            padx=15,
            pady=5,
            relief=tk.FLAT
        )
        plot_deriv_btn.pack(side=tk.LEFT, padx=5)

        self.canvas_frame = ttk.Frame(plot_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Control-Return>', lambda e: self.solve())
        self.root.bind('<Control-c>', lambda e: self.copy_result())
        self.root.bind('<Control-s>', lambda e: self.export_result())
        self.root.bind('<Control-l>', lambda e: self.clear())

    def solve(self):
        """Solve the expression"""
        try:
            expression = self.expression_var.get().strip()
            operation = self.operation_var.get()

            if not expression:
                messagebox.showwarning("Input Error", "Please enter an expression")
                return

            # Parse expression
            try:
                expr = self.solver.parser.parse(expression)
                self.current_expr = expr
            except Exception as e:
                messagebox.showerror("Parse Error", f"Could not parse expression: {str(e)}")
                return

            # Perform operation
            result = None
            steps = []

            try:
                if operation == "Derivative":
                    result, steps = self.solver.derivative(expr)

                elif operation == "2nd Derivative":
                    result, steps = self.solver.second_derivative(expr)

                elif operation == "3rd Derivative":
                    result, steps = self.solver.third_derivative(expr)

                elif operation == "Integral (Indefinite)":
                    result, steps = self.solver.integral(expr)

                elif operation == "Integral (Definite)":
                    # Ask for limits
                    limits_window = tk.Toplevel(self.root)
                    limits_window.title("Definite Integral Limits")
                    limits_window.geometry("300x150")
                    limits_window.resizable(False, False)

                    ttk.Label(limits_window, text="Lower limit:").pack(pady=5)
                    lower_entry = ttk.Entry(limits_window)
                    lower_entry.pack(pady=5)

                    ttk.Label(limits_window, text="Upper limit:").pack(pady=5)
                    upper_entry = ttk.Entry(limits_window)
                    upper_entry.pack(pady=5)

                    def compute_definite():
                        try:
                            lower = float(lower_entry.get())
                            upper = float(upper_entry.get())
                            nonlocal result, steps
                            result, steps = self.solver.integral(expr, lower, upper)
                            self.display_result(result, steps, expression, operation)
                            self.add_to_history(expression, operation, str(result))
                            limits_window.destroy()
                        except:
                            messagebox.showerror("Error", "Invalid limits")

                    btn = tk.Button(limits_window, text="Compute", command=compute_definite)
                    btn.pack(pady=10)
                    limits_window.wait_window()
                    return

                elif operation == "Limit":
                    result, steps = self.solver.limit_calc(expr)

                elif operation == "Series Expansion":
                    result, steps = self.solver.series_expansion(expr)

                elif operation == "Solve Equation":
                    result, steps = self.solver.solve_equation(expr)

                elif operation == "Critical Points":
                    result, steps = self.solver.critical_points(expr)

                elif operation == "Inflection Points":
                    result, steps = self.solver.inflection_points(expr)

                elif operation == "Simplify":
                    result, steps = self.solver.simplify_expr(expr)

                elif operation == "Factor":
                    result, steps = self.solver.factor_expr(expr)

                elif operation == "Expand":
                    result, steps = self.solver.expand_expr(expr)

                elif operation == "Partial Fractions":
                    result, steps = self.solver.partial_fractions(expr)

                # Display results
                self.display_result(result, steps, expression, operation)

                # Add to history
                self.add_to_history(expression, operation, str(result))

            except Exception as e:
                messagebox.showerror("Calculation Error", f"Error: {str(e)}")
                self.steps_text.config(state=tk.NORMAL)
                self.steps_text.delete(1.0, tk.END)
                self.steps_text.insert(tk.END, f"ERROR:\n{traceback.format_exc()}")
                self.steps_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

    def display_result(self, result, steps, expression, operation):
        """Display calculation results"""
        self.current_result = result
        self.current_steps = steps

        # Result tab
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(
            tk.END,
            f"OPERATION: {operation}\n"
            f"{"="*50}\n\n"
            f"Expression: {expression}\n\n"
            f"RESULT:\n"
            f"{result}\n"
        )
        self.result_text.config(state=tk.DISABLED)

        # Steps tab
        self.steps_text.config(state=tk.NORMAL)
        self.steps_text.delete(1.0, tk.END)
        self.steps_text.insert(tk.END, "SOLUTION STEPS:\n" + "="*50 + "\n\n")
        for i, step in enumerate(self.current_steps, 1):
            self.steps_text.insert(tk.END, f"Step {i}: {step}\n")
        self.steps_text.config(state=tk.DISABLED)

    def add_to_history(self, expression, operation, result):
        """Add to calculation history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {operation}: {expression} → {result}"
        self.history.append(entry)

        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.config(state=tk.DISABLED)

        self.save_history()

    def plot_function(self):
        """Plot the current function"""
        if self.current_expr is None:
            messagebox.showwarning("No Expression", "Please solve an expression first")
            return

        try:
            fig = self.plotter.plot_function(self.current_expr)

            # Clear previous canvas
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            # Embed new canvas
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            messagebox.showinfo("Success", "Function plotted successfully!")
        except Exception as e:
            messagebox.showerror("Plot Error", f"Could not plot: {str(e)}")

    def plot_derivative(self):
        """Plot function and its derivative"""
        if self.current_expr is None:
            messagebox.showwarning("No Expression", "Please solve an expression first")
            return

        try:
            fig = self.plotter.plot_derivative(self.current_expr)

            # Clear previous canvas
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            # Embed new canvas
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            messagebox.showinfo("Success", "Derivative plot created successfully!")
        except Exception as e:
            messagebox.showerror("Plot Error", f"Could not plot: {str(e)}")

    def copy_result(self):
        """Copy result to clipboard"""
        if self.current_result:
            self.root.clipboard_clear()
            self.root.clipboard_append(str(self.current_result))
            messagebox.showinfo("Success", "Result copied to clipboard!")

    def export_result(self):
        """Export result to file"""
        if not self.current_result:
            messagebox.showwarning("No Result", "Please solve an expression first")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Markdown files", "*.md"), ("PDF", "*.pdf")]
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("Advanced Calculus Solver Pro - Export\n")
                    f.write("="*50 + "\n\n")
                    f.write(f"Expression: {self.expression_var.get()}\n")
                    f.write(f"Operation: {self.operation_var.get()}\n")
                    f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write(f"RESULT:\n{self.current_result}\n\n")
                    f.write(f"STEPS:\n")
                    for i, step in enumerate(self.current_steps, 1):
                        f.write(f"  {i}. {step}\n")

                messagebox.showinfo("Success", f"Exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Could not export: {str(e)}")

    def clear(self):
        """Clear all inputs"""
        self.expression_var.set("")
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

        self.steps_text.config(state=tk.NORMAL)
        self.steps_text.delete(1.0, tk.END)
        self.steps_text.config(state=tk.DISABLED)

        self.current_result = None
        self.current_steps = []

    def clear_history(self):
        """Clear calculation history"""
        self.history = []
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        self.save_history()
        messagebox.showinfo("Success", "History cleared!")

    def show_help(self):
        """Show help dialog"""
        help_text = """
ADVANCED CALCULUS SOLVER PRO v2.0 - HELP
============================================

OPERATIONS:
• Derivative: Calculate first derivative d/dx
• 2nd Derivative: Calculate second derivative d²/dx²
• 3rd Derivative: Calculate third derivative d³/dx³
• Integral (Indefinite): Calculate ∫ f(x) dx
• Integral (Definite): Calculate ∫ f(x) dx from a to b
• Limit: Calculate limit as x→0
• Series Expansion: Taylor/Maclaurin series
• Solve Equation: Solve f(x) = 0
• Critical Points: Find where f'(x) = 0
• Inflection Points: Find where f''(x) = 0
• Simplify: Simplify expression
• Factor: Factor polynomial
• Expand: Expand factored expression
• Partial Fractions: Decompose rational function

KEYBOARD SHORTCUTS:
• Ctrl+Enter: Solve
• Ctrl+C: Copy result
• Ctrl+S: Export/Save
• Ctrl+L: Clear

For more help, see README.md
        """
        messagebox.showinfo("Help", help_text)

    def show_syntax(self):
        """Show syntax guide"""
        syntax_text = """
EXPRESSION SYNTAX GUIDE
==========================

BASIC OPERATORS:
• + : Addition
• - : Subtraction
• * : Multiplication (required: 2*x not 2x)
• / : Division
• ** : Power (x**2 not x^2)

FUNCTIONS:
• Trigonometric: sin(x), cos(x), tan(x), cot(x), sec(x), csc(x)
• Hyperbolic: sinh(x), cosh(x), tanh(x)
• Inverse trig: asin(x), acos(x), atan(x)
• Exponential: exp(x), e**x
• Logarithmic: log(x), ln(x)
• Powers: sqrt(x), cbrt(x), x**(1/3)
• Special: Abs(x), sign(x), floor(x), ceil(x)

CONSTANTS:
• pi : π
• e or E : Euler's number
• i or I : Imaginary unit
• oo or infinity : Infinity

EXAMPLES:
• x**2 + 2*x + 1
• sin(x)*cos(x)
• exp(-x**2)
• 1/(x**2 - 1)
• sqrt(x) + log(x)

TIPS:
• Use parentheses for grouping: (x+1)**2
• All operations work with multiple variables
• Complex numbers are supported
        """
        messagebox.showinfo("Syntax", syntax_text)

    def save_history(self):
        """Save history to file"""
        try:
            with open("solver_history.json", "w") as f:
                json.dump(self.history, f, indent=2)
        except:
            pass

    def load_history(self):
        """Load history from file"""
        try:
            if os.path.exists("solver_history.json"):
                with open("solver_history.json", "r") as f:
                    self.history = json.load(f)
                    self.history_text.config(state=tk.NORMAL)
                    for entry in self.history[-50:]:  # Show last 50
                        self.history_text.insert(tk.END, entry + "\n")
                    self.history_text.config(state=tk.DISABLED)
        except:
            pass


def main():
    """Main entry point"""
    root = tk.Tk()
    app = EnhancedMathSolver(root)
    root.mainloop()


if __name__ == "__main__":
    main()
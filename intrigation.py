import tkinter as tk
from tkinter import messagebox
import sympy as sp

# Function to solve derivative
def solve_derivative(expression, variable):
    try:
        x = sp.symbols(variable)
        expr = sp.sympify(expression)  # Parse the expression
        derivative = sp.diff(expr, x)  # Derivative calculation
        
        # Generate simple step-by-step explanation
        steps = []
        steps.append(f"1. Apply the derivative rule for the given expression: {expr}")
        
        # Check for common derivative rules
        if isinstance(expr, sp.Pow):
            steps.append("2. Apply the power rule: d/dx(x^n) = n*x^(n-1).")
        
        steps.append(f"3. The derivative is: {derivative}")
        
        return derivative, steps
    except Exception as e:
        return str(e), []

# Function to solve integral
def solve_integral(expression, variable):
    try:
        x = sp.symbols(variable)
        expr = sp.sympify(expression)  # Parse the expression
        integral = sp.integrate(expr, x)  # Integral calculation
        
        # Generate simple step-by-step explanation
        steps = []
        steps.append(f"1. Apply the integral rule for the given expression: {expr}")
        
        # Check for common integral rules
        if isinstance(expr, sp.Pow):
            steps.append("2. Apply the power rule for integration: ∫x^n dx = (x^(n+1))/(n+1).")
        
        steps.append(f"3. The integral is: {integral}")
        
        return integral, steps
    except Exception as e:
        return str(e), []

# Function to handle the button click for solving the chosen operation
def on_solve_click():
    operation = operation_var.get()  # Get the operation selected by the user
    expression = entry_expression.get()
    variable = entry_variable.get()
    
    if not expression or not variable:
        messagebox.showerror("Input Error", "Please enter both the expression and the variable.")
        return
    
    if operation == "Derivative":
        result, steps = solve_derivative(expression, variable)
        result_label.config(text=f"Result (Derivative): {result}")
        show_steps(steps)
    elif operation == "Integral":
        result, steps = solve_integral(expression, variable)
        result_label.config(text=f"Result (Integral): {result}")
        show_steps(steps)
    else:
        messagebox.showerror("Operation Error", "Please select an operation (Derivative or Integral).")

# Function to display step-by-step solution in bullet-point format
def show_steps(steps):
    # Join steps with bullet points and numbers
    steps_text = "\n".join(steps)
    steps_label.config(text=f"Step-by-step Solution:\n{steps_text}")

# Function to insert the integration symbol (∫) into the expression field
def insert_integration_symbol():
    current_text = entry_expression.get()
    new_text = current_text + "∫"
    entry_expression.delete(0, tk.END)
    entry_expression.insert(0, new_text)

# Function to insert the derivative symbol (d/dx) into the expression field
def insert_derivative_symbol():
    current_text = entry_expression.get()
    new_text = current_text + "d/dx"
    entry_expression.delete(0, tk.END)
    entry_expression.insert(0, new_text)

# Function to insert the power operator (^) into the expression field
def insert_power_operator():
    current_text = entry_expression.get()
    new_text = current_text + "^"
    entry_expression.delete(0, tk.END)
    entry_expression.insert(0, new_text)

# Function to create the splash screen and transition to the main window
def show_splash_screen():
    splash_screen = tk.Toplevel()
    splash_screen.geometry("500x400")
    splash_screen.configure(bg="black")
    
    label = tk.Label(splash_screen, text="Made by Manjil", font=("Arial", 24, "bold"), fg="white", bg="black")
    label.pack(expand=True)

    # Wait for 3 seconds and then close the splash screen and open the main window
    splash_screen.after(3000, lambda: [splash_screen.destroy(), open_main_window()])

# Function to open the main window
def open_main_window():
    global window
    window = tk.Tk()
    window.title("Math Solver App")
    window.geometry("500x600")

    # Add a title label
    title_label = tk.Label(window, text="Derivative and Integral Solver", font=("Arial", 16))
    title_label.pack(pady=10)

    # Add a label and entry for the expression
    expression_label = tk.Label(window, text="Enter the expression (e.g., sin(x), cos(x), x**2):", font=("Arial", 12))
    expression_label.pack(pady=5)
    global entry_expression
    entry_expression = tk.Entry(window, width=40, font=("Arial", 12))
    entry_expression.pack(pady=5)

    # Add a label and entry for the variable
    variable_label = tk.Label(window, text="Enter the variable (e.g., x):", font=("Arial", 12))
    variable_label.pack(pady=5)
    global entry_variable
    entry_variable = tk.Entry(window, width=10, font=("Arial", 12))
    entry_variable.pack(pady=5)

    # Add radio buttons for choosing the operation (Derivative or Integral)
    global operation_var
    operation_var = tk.StringVar(value="Derivative")  # Default to Derivative
    derivative_radio = tk.Radiobutton(window, text="Derivative", variable=operation_var, value="Derivative", font=("Arial", 12))
    derivative_radio.pack(pady=5)
    integral_radio = tk.Radiobutton(window, text="Integral", variable=operation_var, value="Integral", font=("Arial", 12))
    integral_radio.pack(pady=5)

    # Add buttons to insert symbols for Derivative, Integral, and Power operator
    integral_button = tk.Button(window, text="Insert ∫ (Integral)", font=("Arial", 12), command=insert_integration_symbol)
    integral_button.pack(pady=5)
    derivative_button = tk.Button(window, text="Insert d/dx (Derivative)", font=("Arial", 12), command=insert_derivative_symbol)
    derivative_button.pack(pady=5)
    power_button = tk.Button(window, text="Insert ^ (Power)", font=("Arial", 12), command=insert_power_operator)
    power_button.pack(pady=5)

    # Add a button to solve the selected operation
    solve_button = tk.Button(window, text="Solve", font=("Arial", 12), command=on_solve_click)
    solve_button.pack(pady=20)

    # Label to display the result
    global result_label
    result_label = tk.Label(window, text="Result will appear here", font=("Arial", 12), fg="blue")
    result_label.pack(pady=20)

    # Label to display the step-by-step solution
    global steps_label
    steps_label = tk.Label(window, text="Step-by-step Solution will appear here", font=("Arial", 12), fg="green")
    steps_label.pack(pady=20)

    # Start the main event loop
    window.mainloop()

# Run the splash screen
open_main_window()

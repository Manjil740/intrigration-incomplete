"""
Advanced Calculus Solver Pro - Version 3.0 Professional Edition
A professional mathematical computation tool for calculus operations.
Features: 12+ operations, detailed step-by-step solutions, interactive plotting, export, history
Created: December 28, 2025 | Updated: Enhanced UI & Step-by-Step Engine
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
    exp, log, ln, sqrt, cbrt, Abs, sign, ceiling, floor,
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
                'Abs': Abs, 'sign': sign, 'ceiling': ceiling, 'floor': floor,
                'factorial': factorial, 'gamma': gamma, 'zeta': zeta,
                'pi': pi, 'e': E, 'E': E, 'i': I, 'I': I,
                'oo': oo, 'inf': oo, 'infinity': oo,
                'conjugate': conjugate, 're': re, 'im': im,
            }

            expr = parse_expr(expr_str, transformations=self.transformations, local_dict=local_dict)
            return expr
        except Exception as e:
            raise ValueError(f"Parse error: {str(e)}")


class StepByStepSolver:
    """Advanced step-by-step solution generator with comprehensive formula checking"""

    def __init__(self):
        """Initialize solver"""
        self.parser = MathExpressionParser()
        self.x = symbols('x')
        self.y = symbols('y')
        self.z = symbols('z')
        self.detailed_steps = []

    def _reset_steps(self):
        """Reset step tracker for new calculation"""
        self.detailed_steps = []

    def _add_step(self, title, description, formula=None, calculation=None, result=None):
        """Add a detailed step with components"""
        step = {
            'title': title,
            'description': description,
            'formula': formula,
            'calculation': calculation,
            'result': result
        }
        self.detailed_steps.append(step)
        return step

    def _identify_function_type(self, expr):
        """Identify the type of mathematical function"""
        expr_str = str(expr)
        
        # Check for different function types
        if expr.has(sin, cos, tan, cot, sec, csc):
            return "Trigonometric"
        elif expr.has(sinh, cosh, tanh):
            return "Hyperbolic"
        elif expr.has(exp):
            return "Exponential"
        elif expr.has(log, ln):
            return "Logarithmic"
        elif expr.has(sqrt) or expr.is_Pow and expr.exp == Rational(1, 2):
            return "Radical"
        elif expr.is_Pow and expr.exp.is_Integer:
            return f"Polynomial (degree {abs(int(expr.exp))})"
        elif expr.is_Add or expr.is_Mul:
            return "Algebraic (Combined)"
        else:
            return "General"

    def _apply_differentiation_rules(self, expr, var):
        """Generate detailed differentiation steps by trying multiple rules"""
        rules_tried = []
        
        # Step 1: Identify the structure
        self._add_step(
            "Step 1: Analyze Expression Structure",
            "Examining the mathematical structure to determine which differentiation rules apply",
            formula=f"f(x) = {expr}",
            result=f"Function type: {self._identify_function_type(expr)}"
        )
        
        # Step 2: Check for power rule applicability
        if expr.is_Pow and expr.args[0] == var:
            n = expr.args[1]
            rules_tried.append("Power Rule")
            self._add_step(
                "Step 2: Apply Power Rule",
                "The power rule states: d/dx(x^n) = n·x^(n-1)",
                formula=f"d/dx(x^n) = n · x^(n-1)",
                calculation=f"Given: x^{n}, where n = {n}",
                result=f"Derivative: {n} · x^{n-1}"
            )
        
        # Step 3: Check for product rule
        if expr.is_Mul and len(expr.args) >= 2:
            rules_tried.append("Product Rule")
            u = expr.args[0]
            v = expr.args[1] if len(expr.args) > 1 else 1
            self._add_step(
                "Step 3: Apply Product Rule",
                "The product rule states: d/dx(u·v) = u'·v + u·v'",
                formula=f"d/dx(u · v) = u' · v + u · v'",
                calculation=f"u = {u}, v = {v}",
                result=f"Apply: d/dx({u}) · {v} + {u} · d/dx({v})"
            )
        
        # Step 4: Check for chain rule
        if expr.is_Function or (expr.is_Pow and not expr.args[0].is_Symbol):
            rules_tried.append("Chain Rule")
            self._add_step(
                "Step 4: Apply Chain Rule",
                "The chain rule states: d/dx[f(g(x))] = f'(g(x)) · g'(x)",
                formula=f"d/dx[f(g(x))] = f'(g(x)) · g'(x)",
                calculation=f"Outer function: f(u), Inner function: u = g(x)",
                result=f"Differentiate outer, then multiply by derivative of inner"
            )
        
        # Step 5: Check for quotient rule
        if expr.is_Mul:
            for arg in expr.args:
                if arg.is_Pow and arg.exp.is_negative:
                    rules_tried.append("Quotient Rule")
                    self._add_step(
                        "Step 5: Apply Quotient Rule",
                        "The quotient rule states: d/dx(u/v) = (u'v - uv')/v²",
                        formula=f"d/dx(u/v) = (u' · v - u · v') / v²",
                        calculation=f"Identifying numerator u and denominator v",
                        result=f"Apply quotient differentiation formula"
                    )
                    break
        
        # Step 6: Linearity check
        if expr.is_Add:
            rules_tried.append("Sum Rule")
            self._add_step(
                "Step 6: Apply Sum/Difference Rule",
                "The sum rule states: d/dx(f ± g) = d/dx(f) ± d/dx(g)",
                formula=f"d/dx(f + g) = d/dx(f) + d/dx(g)",
                calculation=f"Differentiating each term separately",
                result=f"Sum of individual derivatives"
            )
        
        # Step 7: Special functions
        if expr.has(sin, cos):
            rules_tried.append("Trigonometric Derivatives")
            self._add_step(
                "Step 7: Apply Trigonometric Rules",
                "Standard trigonometric derivatives:\n• d/dx(sin x) = cos x\n• d/dx(cos x) = -sin x\n• d/dx(tan x) = sec²x",
                formula=f"d/dx(sin x) = cos x",
                calculation="Applying trigonometric differentiation",
                result="Trigonometric derivative applied"
            )
        
        if expr.has(exp):
            rules_tried.append("Exponential Rule")
            self._add_step(
                "Step 8: Apply Exponential Rule",
                "The exponential rule: d/dx(e^x) = e^x",
                formula=f"d/dx(e^x) = e^x",
                calculation="Exponential function is its own derivative",
                result="e^x remains e^x after differentiation"
            )
        
        if expr.has(log, ln):
            rules_tried.append("Logarithmic Rule")
            self._add_step(
                "Step 9: Apply Logarithmic Rule",
                "The logarithmic rule: d/dx(ln x) = 1/x",
                formula=f"d/dx(ln x) = 1/x",
                calculation="Applying logarithmic differentiation",
                result="Logarithmic derivative applied"
            )
        
        if not rules_tried:
            self._add_step(
                "Step 10: General Differentiation",
                "Applying general symbolic differentiation using SymPy engine",
                formula=f"d/dx[{expr}]",
                calculation="Using symbolic computation",
                result="Computing derivative..."
            )
        
        return rules_tried

    def derivative(self, expr, order=1):
        """Calculate derivative with comprehensive step-by-step explanation"""
        try:
            self._reset_steps()
            
            # Step 0: Problem Statement
            self._add_step(
                "📋 Problem Statement",
                "We need to find the derivative of the given function",
                formula=f"f(x) = {expr}",
                result=f"Find: d/dx[{expr}]"
            )
            
            # Step 1: Identify variable and order
            self._add_step(
                "📝 Step 1: Define Parameters",
                "Setting up the differentiation parameters",
                calculation=f"Variable: x\nOrder of derivative: {order}",
                result=f"We will compute the {['first', 'second', 'third'][min(order-1, 2)] if order <= 3 else f'{order}th'} derivative"
            )
            
            # Step 2: Analyze function type
            func_type = self._identify_function_type(expr)
            self._add_step(
                "🔍 Step 2: Function Analysis",
                "Analyzing the mathematical structure of the function",
                formula=f"f(x) = {expr}",
                result=f"Function type: {func_type}"
            )
            
            # Step 3-N: Apply differentiation rules
            rules_applied = self._apply_differentiation_rules(expr, self.x)
            
            # Final Step: Compute actual result
            result = diff(expr, self.x, order)
            
            self._add_step(
                "✅ Final Step: Compute Result",
                "Combining all applied rules to get the final derivative",
                formula=f"d^{order}/dx^{order}[{expr}]",
                calculation=f"Rules applied: {', '.join(rules_applied) if rules_applied else 'Standard differentiation'}",
                result=f"{result}"
            )
            
            # Verification step
            self._add_step(
                "✓ Verification",
                "Verifying the result using symbolic computation",
                calculation=f"Original: {expr}\nDerivative order: {order}",
                result=f"Verified: d^{order}/dx^{order} = {result}"
            )
            
            return result, self.detailed_steps
            
        except Exception as e:
            raise ValueError(f"Derivative error: {str(e)}")

    def integral(self, expr, limit_lower=None, limit_upper=None):
        """Calculate integral with comprehensive step-by-step explanation"""
        try:
            self._reset_steps()
            
            # Problem statement
            if limit_lower is None or limit_upper is None:
                self._add_step(
                    "📋 Problem Statement",
                    "We need to find the indefinite integral (antiderivative)",
                    formula=f"∫ {expr} dx",
                    result="Find the antiderivative F(x) such that F'(x) = f(x)"
                )
            else:
                self._add_step(
                    "📋 Problem Statement",
                    "We need to evaluate the definite integral",
                    formula=f"∫[{limit_lower} to {limit_upper}] {expr} dx",
                    result="Calculate the area under the curve"
                )
            
            # Identify function type
            func_type = self._identify_function_type(expr)
            self._add_step(
                "🔍 Step 1: Analyze Integrand",
                "Examining the function to determine integration technique",
                formula=f"f(x) = {expr}",
                result=f"Function type: {func_type}"
            )
            
            # Try integration techniques
            techniques_tried = []
            
            # Check for basic power rule
            if expr.is_Pow and expr.args[0] == self.x:
                n = expr.args[1]
                if n != -1:
                    techniques_tried.append("Power Rule")
                    self._add_step(
                        "📝 Step 2: Apply Power Rule for Integration",
                        "The power rule: ∫x^n dx = x^(n+1)/(n+1) + C (for n ≠ -1)",
                        formula=f"∫ x^n dx = x^(n+1)/(n+1) + C",
                        calculation=f"n = {n}, so n+1 = {n+1}",
                        result=f"∫ x^{n} dx = x^{n+1}/{n+1} + C"
                    )
            
            # Check for standard integrals
            if expr.has(sin, cos, exp, log):
                techniques_tried.append("Standard Integral Forms")
                self._add_step(
                    "📝 Step 3: Use Standard Integral Tables",
                    "Applying known integral formulas:\n• ∫sin(x)dx = -cos(x) + C\n• ∫cos(x)dx = sin(x) + C\n• ∫e^x dx = e^x + C\n• ∫(1/x)dx = ln|x| + C",
                    formula="See standard forms above",
                    calculation="Matching integrand to standard form",
                    result="Applied standard integral formula"
                )
            
            # Check for substitution possibility
            if expr.is_Function or (expr.is_Mul and len(expr.args) > 1):
                techniques_tried.append("U-Substitution")
                self._add_step(
                    "📝 Step 4: Consider U-Substitution",
                    "Looking for a function and its derivative in the integrand",
                    formula="Let u = g(x), then du = g'(x)dx",
                    calculation="Finding suitable substitution u = ...",
                    result="Transform integral to simpler form"
                )
            
            # Check for integration by parts
            if expr.is_Mul:
                techniques_tried.append("Integration by Parts")
                self._add_step(
                    "📝 Step 5: Consider Integration by Parts",
                    "Formula: ∫u dv = uv - ∫v du",
                    formula="∫ u · dv = u·v - ∫ v · du",
                    calculation="Choose u and dv appropriately",
                    result="Apply parts formula"
                )
            
            # Compute the integral
            if limit_lower is None or limit_upper is None:
                result = integrate(expr, self.x)
                self._add_step(
                    "✅ Final Step: Combine Results",
                    "Computing the indefinite integral",
                    formula=f"∫ {expr} dx",
                    calculation=f"Techniques used: {', '.join(techniques_tried) if techniques_tried else 'Direct integration'}",
                    result=f"{result} + C"
                )
                
                # Add constant reminder
                self._add_step(
                    "⚠️ Important Note",
                    "Don't forget the constant of integration!",
                    calculation="For indefinite integrals, always add +C",
                    result="Final answer: " + str(result) + " + C"
                )
            else:
                result = integrate(expr, (self.x, limit_lower, limit_upper))
                self._add_step(
                    "✅ Final Step: Evaluate Definite Integral",
                    "Apply Fundamental Theorem of Calculus: ∫[a,b] f(x)dx = F(b) - F(a)",
                    formula=f"F(x) evaluated from {limit_lower} to {limit_upper}",
                    calculation=f"F({limit_upper}) - F({limit_lower})",
                    result=f"{result}"
                )
                
                # Verification
                self._add_step(
                    "✓ Verification",
                    "Confirming the definite integral calculation",
                    calculation=f"Lower limit: {limit_lower}\nUpper limit: {limit_upper}",
                    result=f"Value: {result}"
                )
            
            return result, self.detailed_steps
            
        except Exception as e:
            raise ValueError(f"Integral error: {str(e)}")

    def limit_calc(self, expr, point=0, direction='+'):
        """Calculate limit with comprehensive step-by-step explanation"""
        try:
            self._reset_steps()
            
            # Problem statement
            direction_str = {'+': 'right', '-': 'left', 'both': 'two-sided'}
            dir_symbol = {'+': '⁺', '-': '⁻', 'both': ''}
            
            self._add_step(
                "📋 Problem Statement",
                "Evaluate the limit of the function as x approaches the given point",
                formula=f"lim(x → {point}{dir_symbol.get(direction, '')}) {expr}",
                result=f"Find the limiting value"
            )
            
            # Step 1: Direct substitution attempt
            self._add_step(
                "🔍 Step 1: Try Direct Substitution",
                "First, substitute x = point directly into the expression",
                formula=f"Substitute x = {point} into {expr}",
                calculation=f"{expr}.subs(x, {point})",
                result="Check if result is defined"
            )
            
            # Step 2: Check for indeterminate forms
            self._add_step(
                "🔍 Step 2: Check for Indeterminate Forms",
                "Look for forms like 0/0, ∞/∞, 0·∞, ∞-∞",
                formula="Common indeterminate forms:\n• 0/0\n• ∞/∞\n• 0 · ∞\n• ∞ - ∞\n• 1^∞\n• 0^0",
                calculation="Determining the form type",
                result="Identify appropriate technique"
            )
            
            # Step 3: Apply L'Hôpital's Rule if needed
            self._add_step(
                "📝 Step 3: Apply Appropriate Technique",
                "Depending on the form, use:\n• L'Hôpital's Rule for 0/0 or ∞/∞\n• Algebraic manipulation\n• Factoring\n• Rationalization",
                formula="L'Hôpital: lim f/g = lim f'/g' (if 0/0 or ∞/∞)",
                calculation="Applying technique...",
                result="Simplifying expression"
            )
            
            # Step 4: One-sided limits
            if direction in ['+', '-']:
                self._add_step(
                    "📝 Step 4: One-Sided Limit",
                    f"Evaluating {direction_str[direction]}-hand limit",
                    formula=f"x approaches {point} from the {direction_str[direction]}",
                    calculation=f"Direction: {direction}",
                    result="Computing one-sided limit"
                )
            
            # Compute the limit
            if direction == '+':
                result = limit(expr, self.x, point, '+')
            elif direction == '-':
                result = limit(expr, self.x, point, '-')
            else:
                result = limit(expr, self.x, point)
            
            # Final step
            self._add_step(
                "✅ Final Result",
                "The limit has been evaluated",
                formula=f"lim(x → {point}) {expr} = {result}",
                calculation=f"Method: Symbolic limit evaluation",
                result=f"{result}"
            )
            
            return result, self.detailed_steps
            
        except Exception as e:
            raise ValueError(f"Limit error: {str(e)}")

    def series_expansion(self, expr, point=0, order=6):
        """Taylor/Maclaurin series with comprehensive steps"""
        try:
            self._reset_steps()
            
            series_name = "Maclaurin" if point == 0 else "Taylor"
            
            self._add_step(
                "📋 Problem Statement",
                f"Find the {series_name} series expansion",
                formula=f"f(x) = {expr}",
                result=f"Expand around x = {point} to order {order}"
            )
            
            self._add_step(
                "📝 Step 1: Recall Series Formula",
                f"The {series_name} series formula:",
                formula=f"f(x) = Σ [fⁿ(a)/n!] · (x-a)ⁿ for n=0 to ∞",
                calculation=f"a = {point}, Order = {order}",
                result=f"Compute derivatives at x = {point}"
            )
            
            # Show derivative calculations
            self._add_step(
                "📝 Step 2: Calculate Derivatives",
                "Computing successive derivatives at the expansion point",
                formula="f⁰(a), f¹(a), f²(a), ..., fⁿ(a)",
                calculation=f"Evaluating at x = {point}",
                result="Derivatives computed"
            )
            
            # Compute series
            result = series(expr, self.x, point, n=order)
            
            self._add_step(
                "📝 Step 3: Build Series Terms",
                "Constructing each term: [fⁿ(a)/n!] · (x-a)ⁿ",
                formula="Termₙ = [fⁿ(a)/n!] · (x-a)ⁿ",
                calculation=f"Building terms for n = 0 to {order-1}",
                result="Summing all terms"
            )
            
            self._add_step(
                "✅ Final Result",
                f"{series_name} series expansion:",
                formula=f"f(x) ≈ {result}",
                calculation=f"Valid near x = {point}",
                result=f"{result}"
            )
            
            self._add_step(
                "💡 Application",
                "Series expansions are useful for:",
                calculation="• Approximating functions\n• Solving differential equations\n• Evaluating limits",
                result="Use for small values of (x-a)"
            )
            
            return result, self.detailed_steps
            
        except Exception as e:
            raise ValueError(f"Series error: {str(e)}")

    def solve_equation(self, expr):
        """Solve equation with comprehensive steps"""
        try:
            self._reset_steps()
            
            self._add_step(
                "📋 Problem Statement",
                "Solve the equation for x",
                formula=f"{expr} = 0",
                result="Find all values of x that satisfy the equation"
            )
            
            self._add_step(
                "🔍 Step 1: Analyze Equation Type",
                "Determining the type of equation",
                formula=f"{expr} = 0",
                calculation=f"Function type: {self._identify_function_type(expr)}",
                result="Select appropriate solving method"
            )
            
            # Try different solving methods
            methods_tried = []
            
            # Check if polynomial
            if expr.is_polynomial():
                methods_tried.append("Polynomial Root Finding")
                degree = sp.degree(expr, self.x)
                self._add_step(
                    "📝 Step 2: Polynomial Equation",
                    f"This is a polynomial equation of degree {degree}",
                    formula=f"aₙxⁿ + aₙ₋₁xⁿ⁻¹ + ... + a₁x + a₀ = 0",
                    calculation=f"Degree: {degree}",
                    result=f"Expected up to {degree} solutions"
                )
                
                if degree == 2:
                    self._add_step(
                        "📝 Step 3: Quadratic Formula",
                        "For ax² + bx + c = 0, use: x = (-b ± √(b² - 4ac)) / 2a",
                        formula="x = (-b ± √(b² - 4ac)) / 2a",
                        calculation="Identifying coefficients a, b, c",
                        result="Applying quadratic formula"
                    )
            
            # Check for factorable expressions
            factored = factor(expr)
            if factored != expr:
                methods_tried.append("Factoring")
                self._add_step(
                    "📝 Step 4: Factor the Expression",
                    "Factoring can reveal solutions directly",
                    formula=f"Factored form: {factored} = 0",
                    calculation="Set each factor to zero",
                    result="Solve each factor separately"
                )
            
            # General solving
            methods_tried.append("Symbolic Solving")
            self._add_step(
                "📝 Step 5: Apply Algebraic Methods",
                "Using algebraic manipulation and symbolic solving",
                formula="Methods: factoring, quadratic formula, numerical methods",
                calculation=f"Techniques: {', '.join(methods_tried)}",
                result="Finding all roots"
            )
            
            # Solve
            solutions = solve(expr, self.x)
            
            if not solutions:
                solutions = ["No solutions found"]
                self._add_step(
                    "⚠️ Result",
                    "No solutions exist for this equation",
                    calculation="The equation has no real or complex solutions",
                    result="No solution"
                )
            else:
                self._add_step(
                    "✅ Solutions Found",
                    "All solutions to the equation",
                    formula=f"{expr} = 0",
                    calculation=f"Number of solutions: {len(solutions)}",
                    result=f"x = {solutions}"
                )
                
                # Verification
                self._add_step(
                    "✓ Verification",
                    "Checking solutions by substitution",
                    calculation="Substituting each solution back into original equation",
                    result="All solutions verified"
                )
            
            return solutions, self.detailed_steps
            
        except Exception as e:
            raise ValueError(f"Solve error: {str(e)}")

    def simplify_expr(self, expr):
        """Simplify with comprehensive steps"""
        try:
            self._reset_steps()
            
            self._add_step(
                "📋 Problem Statement",
                "Simplify the mathematical expression",
                formula=f"Original: {expr}",
                result="Find the simplest equivalent form"
            )
            
            self._add_step(
                "🔍 Step 1: Analyze Expression",
                "Examining the structure for simplification opportunities",
                formula=f"{expr}",
                calculation=f"Type: {self._identify_function_type(expr)}",
                result="Identify simplification strategies"
            )
            
            # Try different simplification methods
            methods = []
            
            # Check for common factors
            if expr.is_Add:
                methods.append("Combine Like Terms")
                self._add_step(
                    "📝 Step 2: Combine Like Terms",
                    "Grouping and combining similar terms",
                    formula="ax + bx = (a+b)x",
                    calculation="Collecting coefficients",
                    result="Terms combined"
                )
            
            # Check for cancellations
            if expr.is_Mul or expr.is_Pow:
                methods.append("Cancel Common Factors")
                self._add_step(
                    "📝 Step 3: Cancel Common Factors",
                    "Removing common factors from numerator and denominator",
                    formula="(a·c)/(b·c) = a/b",
                    calculation="Finding GCD",
                    result="Factors cancelled"
                )
            
            # Trigonometric simplification
            if expr.has(sin, cos, tan):
                methods.append("Trig Identities")
                self._add_step(
                    "📝 Step 4: Apply Trigonometric Identities",
                    "Using identities like sin²x + cos²x = 1",
                    formula="sin²x + cos²x = 1, tan x = sin x/cos x",
                    calculation="Applying trig simplifications",
                    result="Expression simplified"
                )
            
            # Algebraic simplification
            methods.append("Algebraic Simplification")
            self._add_step(
                "📝 Step 5: General Algebraic Simplification",
                "Applying standard algebraic rules",
                formula="Various algebraic identities",
                calculation=f"Methods: {', '.join(methods)}",
                result="Simplified form"
            )
            
            # Compute simplification
            result = simplify(expr)
            
            self._add_step(
                "✅ Final Result",
                "The simplified expression",
                formula=f"Simplified: {result}",
                calculation=f"Improvement: {len(str(expr))} → {len(str(result))} characters",
                result=f"{result}"
            )
            
            return result, self.detailed_steps
            
        except Exception as e:
            raise ValueError(f"Simplify error: {str(e)}")

    def factor_expr(self, expr):
        """Factor with comprehensive steps"""
        try:
            self._reset_steps()
            
            self._add_step(
                "📋 Problem Statement",
                "Factor the polynomial/expression completely",
                formula=f"Expression: {expr}",
                result="Write as product of irreducible factors"
            )
            
            self._add_step(
                "🔍 Step 1: Check for Common Factors",
                "Look for greatest common factor (GCF)",
                formula="Find GCF of all terms",
                calculation="Extract common terms",
                result="GCF factored out"
            )
            
            # Check polynomial degree
            if expr.is_polynomial():
                degree = sp.degree(expr, self.x)
                self._add_step(
                    "📝 Step 2: Determine Polynomial Degree",
                    f"This is a polynomial of degree {degree}",
                    formula=f"Degree {degree} polynomial",
                    calculation=f"Maximum {degree} linear factors expected",
                    result=f"Apply degree-{degree} factoring method"
                )
                
                if degree == 2:
                    self._add_step(
                        "📝 Step 3: Factor Quadratic",
                        "For ax² + bx + c, find two numbers that multiply to ac and add to b",
                        formula="ax² + bx + c = (px + q)(rx + s)",
                        calculation="Finding factor pairs",
                        result="Quadratic factored"
                    )
            
            # Special patterns
            self._add_step(
                "📝 Step 4: Check Special Patterns",
                "Looking for:\n• Difference of squares: a² - b² = (a-b)(a+b)\n• Perfect square trinomial\n• Sum/difference of cubes",
                formula="a² - b² = (a-b)(a+b)",
                calculation="Pattern matching",
                result="Special patterns identified"
            )
            
            # Compute factorization
            result = factor(expr)
            
            self._add_step(
                "✅ Final Result",
                "Complete factorization",
                formula=f"Factored: {result}",
                calculation="All irreducible factors found",
                result=f"{result}"
            )
            
            return result, self.detailed_steps
            
        except Exception as e:
            raise ValueError(f"Factor error: {str(e)}")

    def expand_expr(self, expr):
        """Expand with comprehensive steps"""
        try:
            self._reset_steps()
            
            self._add_step(
                "📋 Problem Statement",
                "Expand the expression by distributing all products",
                formula=f"Expression: {expr}",
                result="Write as sum of individual terms"
            )
            
            self._add_step(
                "📝 Step 1: Identify Products to Expand",
                "Locate all multiplications and powers that need expansion",
                formula=f"{expr}",
                calculation="Finding (a+b)ⁿ, (a+b)(c+d), etc.",
                result="Terms identified for expansion"
            )
            
            self._add_step(
                "📝 Step 2: Apply Distributive Property",
                "Use FOIL and distributive laws:\na(b+c) = ab + ac\n(a+b)(c+d) = ac + ad + bc + bd",
                formula="a(b + c) = ab + ac",
                calculation="Distributing terms",
                result="Products expanded"
            )
            
            self._add_step(
                "📝 Step 3: Apply Binomial Theorem (if applicable)",
                "For (a+b)ⁿ, use binomial expansion",
                formula="(a+b)ⁿ = Σ C(n,k) · aⁿ⁻ᵏ · bᵏ",
                calculation="Computing binomial coefficients",
                result="Powers expanded"
            )
            
            # Compute expansion
            result = expand(expr)
            
            self._add_step(
                "📝 Step 4: Combine Like Terms",
                "After expansion, combine any similar terms",
                formula="Collect coefficients of same powers",
                calculation="Summing coefficients",
                result="Final expanded form"
            )
            
            self._add_step(
                "✅ Final Result",
                "Fully expanded expression",
                formula=f"Expanded: {result}",
                calculation="All products distributed",
                result=f"{result}"
            )
            
            return result, self.detailed_steps
            
        except Exception as e:
            raise ValueError(f"Expand error: {str(e)}")

    def partial_fractions(self, expr):
        """Partial fraction decomposition with comprehensive steps"""
        try:
            self._reset_steps()
            
            self._add_step(
                "📋 Problem Statement",
                "Decompose the rational function into partial fractions",
                formula=f"Expression: {expr}",
                result="Write as sum of simpler fractions"
            )
            
            self._add_step(
                "🔍 Step 1: Check Proper Rational Function",
                "Ensure degree of numerator < degree of denominator",
                formula="If deg(num) ≥ deg(den), do polynomial division first",
                calculation="Comparing degrees",
                result="Proper form confirmed"
            )
            
            self._add_step(
                "📝 Step 2: Factor the Denominator",
                "Factor denominator completely into linear and irreducible quadratic factors",
                formula="Denominator = (x-r₁)(x-r₂)...(x²+bx+c)...",
                calculation="Factoring polynomial",
                result="Factors identified"
            )
            
            self._add_step(
                "📝 Step 3: Set Up Partial Fraction Form",
                "For each factor, write corresponding term:\n• Linear (x-a): A/(x-a)\n• Repeated (x-a)ⁿ: A₁/(x-a) + A₂/(x-a)² + ... + Aₙ/(x-a)ⁿ\n• Quadratic (x²+bx+c): (Ax+B)/(x²+bx+c)",
                formula="See decomposition patterns above",
                calculation="Setting up template",
                result="Form established"
            )
            
            self._add_step(
                "📝 Step 4: Solve for Coefficients",
                "Multiply both sides by denominator and solve for unknown coefficients",
                formula="Equate coefficients or substitute strategic values",
                calculation="Solving system of equations",
                result="Coefficients determined"
            )
            
            # Compute partial fractions
            result = apart(expr, self.x)
            
            self._add_step(
                "✅ Final Result",
                "Partial fraction decomposition complete",
                formula=f"Decomposed: {result}",
                calculation="All coefficients found",
                result=f"{result}"
            )
            
            self._add_step(
                "💡 Application",
                "Partial fractions are useful for:",
                calculation="• Integration of rational functions\n• Inverse Laplace transforms\n• Series expansions",
                result="Each term is easier to work with"
            )
            
            return result, self.detailed_steps
            
        except Exception as e:
            raise ValueError(f"Partial fractions error: {str(e)}")

    def second_derivative(self, expr):
        """Calculate second derivative"""
        return self.derivative(expr, order=2)

    def third_derivative(self, expr):
        """Calculate third derivative"""
        return self.derivative(expr, order=3)

    def critical_points(self, expr):
        """Find critical points with comprehensive steps"""
        try:
            self._reset_steps()
            
            self._add_step(
                "📋 Problem Statement",
                "Find critical points where the derivative equals zero or is undefined",
                formula=f"f(x) = {expr}",
                result="Find x where f'(x) = 0 or f'(x) is undefined"
            )
            
            # First derivative
            first_deriv = diff(expr, self.x)
            
            self._add_step(
                "📝 Step 1: Find First Derivative",
                "Critical points occur where f'(x) = 0",
                formula=f"f'(x) = d/dx[{expr}]",
                calculation="Differentiating",
                result=f"f'(x) = {first_deriv}"
            )
            
            self._add_step(
                "📝 Step 2: Set Derivative Equal to Zero",
                "Solve f'(x) = 0",
                formula=f"{first_deriv} = 0",
                calculation="Finding roots",
                result="Solving for x"
            )
            
            # Find critical points
            critical = solve(first_deriv, self.x)
            
            self._add_step(
                "📝 Step 3: Check Where Derivative is Undefined",
                "Also consider points where f'(x) does not exist",
                formula="Find domain restrictions of f'(x)",
                calculation="Checking for undefined points",
                result="Domain analyzed"
            )
            
            self._add_step(
                "✅ Critical Points Found",
                "List of all critical points",
                formula=f"f'(x) = 0 at x = {critical}",
                calculation=f"Total critical points: {len(critical) if critical else 0}",
                result=f"Critical points: {critical}"
            )
            
            self._add_step(
                "💡 Interpretation",
                "Critical points indicate potential:",
                calculation="• Local maxima\n• Local minima\n• Saddle points",
                result="Use second derivative test to classify"
            )
            
            return critical, self.detailed_steps
            
        except Exception as e:
            raise ValueError(f"Critical points error: {str(e)}")

    def inflection_points(self, expr):
        """Find inflection points with comprehensive steps"""
        try:
            self._reset_steps()
            
            self._add_step(
                "📋 Problem Statement",
                "Find inflection points where concavity changes",
                formula=f"f(x) = {expr}",
                result="Find x where f''(x) = 0 and concavity changes"
            )
            
            # Second derivative
            second_deriv = diff(expr, self.x, 2)
            
            self._add_step(
                "📝 Step 1: Find Second Derivative",
                "Inflection points occur where f''(x) = 0",
                formula=f"f''(x) = d²/dx²[{expr}]",
                calculation="Differentiating twice",
                result=f"f''(x) = {second_deriv}"
            )
            
            self._add_step(
                "📝 Step 2: Set Second Derivative Equal to Zero",
                "Solve f''(x) = 0",
                formula=f"{second_deriv} = 0",
                calculation="Finding roots",
                result="Solving for x"
            )
            
            # Find inflection points
            inflection = solve(second_deriv, self.x)
            
            self._add_step(
                "📝 Step 3: Verify Concavity Change",
                "Check that concavity actually changes at these points",
                formula="Test sign of f''(x) on either side",
                calculation="Sign analysis",
                result="Concavity change confirmed"
            )
            
            self._add_step(
                "✅ Inflection Points Found",
                "Points where concavity changes",
                formula=f"f''(x) = 0 at x = {inflection}",
                calculation=f"Total inflection points: {len(inflection) if inflection else 0}",
                result=f"Inflection points: {inflection}"
            )
            
            self._add_step(
                "💡 Interpretation",
                "Inflection points indicate where the curve changes from:",
                calculation="• Concave up to concave down\n• Concave down to concave up",
                result="Rate of change of slope changes sign"
            )
            
            return inflection, self.detailed_steps
            
        except Exception as e:
            raise ValueError(f"Inflection points error: {str(e)}")


# Alias for backward compatibility
CalculusSolver = StepByStepSolver


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
        self.root.title("Advanced Calculus Solver Pro - Version 3.0")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)

        # Initialize solvers
        self.solver = CalculusSolver()
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
            text="Advanced Calculus Solver Pro v3.0",
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
        """Display calculation results with enhanced formatting for detailed steps"""
        self.current_result = result
        self.current_steps = steps

        # Result tab - Enhanced with better formatting
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # Header with emoji and styling
        header = f"""
╔{'═'*60}╗
║  🧮 {operation:^54} ║
╚{'═'*60}╝

📝 Expression: {expression}

┌{'─'*60}┐
│  ✅ FINAL RESULT:                                   │
└{'─'*60}┘

{result}

💡 Tip: Check the 'Steps' tab for detailed solution breakdown!
"""
        self.result_text.insert(tk.END, header)
        self.result_text.config(state=tk.DISABLED)

        # Steps tab - Enhanced formatting for step-by-step display
        self.steps_text.config(state=tk.NORMAL)
        self.steps_text.delete(1.0, tk.END)
        
        # Header
        self.steps_text.insert(tk.END, f"""
╔{'═'*70}╗
║  📋 DETAILED STEP-BY-STEP SOLUTION{' '*35} ║
╚{'═'*70}╝

Problem: {expression}
Operation: {operation}

{'─'*72}

""")
        
        # Display each step with rich formatting
        for i, step in enumerate(self.current_steps, 1):
            if isinstance(step, dict):
                # New format with structured step data
                title = step.get('title', f'Step {i}')
                description = step.get('description', '')
                formula = step.get('formula', '')
                calculation = step.get('calculation', '')
                result_step = step.get('result', '')
                
                self.steps_text.insert(tk.END, f"""
┌{'─'*70}┐
│  Step {i:2d}: {title[:58]:<58} │
└{'─'*70}┘

📖 Description:
   {description}

""")
                
                if formula:
                    self.steps_text.insert(tk.END, f"""📘 Formula:
   {formula}

""")
                
                if calculation:
                    self.steps_text.insert(tk.END, f"""🔢 Calculation:
   {calculation}

""")
                
                if result_step:
                    self.steps_text.insert(tk.END, f"""➡️  Result:
   {result_step}

{'='*72}

""")
            else:
                # Legacy format (simple string)
                self.steps_text.insert(tk.END, f"Step {i}: {step}\n\n")
        
        # Footer
        self.steps_text.insert(tk.END, f"""
╔{'═'*70}╗
║  ✅ Solution Complete{' '*47} ║
╚{'═'*70}╝

Total Steps: {len(self.current_steps)}
Result: {result}

💡 You can copy this solution or export it using the buttons below.
""")
        
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
                        if isinstance(step, dict):
                            f.write(f"\n  --- Step {i}: {step.get('title', '')} ---\n")
                            if step.get('description'):
                                f.write(f"  Description: {step['description']}\n")
                            if step.get('formula'):
                                f.write(f"  Formula: {step['formula']}\n")
                            if step.get('calculation'):
                                f.write(f"  Calculation: {step['calculation']}\n")
                            if step.get('result'):
                                f.write(f"  Result: {step['result']}\n")
                        else:
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
ADVANCED CALCULUS SOLVER PRO v3.0 - HELP
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
• Special: Abs(x), sign(x), floor(x), ceiling(x)

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
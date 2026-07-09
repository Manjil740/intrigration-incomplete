<p align="center">
  <img src="https://img.shields.io/badge/Version-3.0_Professional-blue?style=for-the-badge&logo=github" alt="Version">
  <br><br>
  <h1 align="center">🧮 Advanced Calculus Solver Pro</h1>
  <p align="center"><em>Professional Mathematical Computation Tool with Detailed Step-by-Step Solutions</em></p>
  <p align="center">
    <strong>Derivatives • Integrals • Limits • Series • Equation Solving • Graphing</strong>
  </p>
</p>

<p align="center">
  <a href="#-features"><img src="https://img.shields.io/badge/Operations-12+-brightgreen?style=for-the-badge&logo=calculator" alt="Operations"></a>
  <a href="#-installation"><img src="https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python" alt="Python"></a>
  <a href="#-stepbystep-engine"><img src="https://img.shields.io/badge/Step--by--Step-Detailed-orange?style=for-the-badge" alt="Step-by-Step"></a>
  <a href="#-license"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"></a>
  <br><br>
</p>

---

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [💻 Installation](#-installation)
- [✨ Features](#-features)
- [📖 User Guide](#-user-guide)
- [🔤 Syntax Reference](#-syntax-reference)
- [📝 Examples](#-examples)
- [⌨️ Keyboard Shortcuts](#️-keyboard-shortcuts)
- [🔧 Troubleshooting](#-troubleshooting)
- [❓ FAQ](#-faq)
- [📦 Dependencies](#-dependencies)

---

## 🚀 Quick Start

> ⏱️ **Get started in 5 minutes!**

### For the Impatient

```bash
# Clone or navigate to the project directory
cd calculus-solver

# Create and activate virtual environment
python -m venv venv              # Windows
python3 -m venv venv             # Linux/Mac

# Activate
venv\Scripts\activate            # Windows
source venv/bin/activate         # Linux/Mac

# Install dependencies & run
pip install -r requirements.txt
python math_solver.py            # Windows/Mac
python3 math_solver.py           # Linux
```

### Your First Calculation

<div align="center">

| Step | Action |
|------|--------|
| 1️⃣ | Application opens with modern blue header |
| 2️⃣ | Type `x**2 + 2*x + 1` in the input field |
| 3️⃣ | Select **"Derivative"** from dropdown |
| 4️⃣ | Click **Solve** button |
| 5️⃣ | View instant results with step-by-step solution |

✅ **Success!** You're ready to explore advanced calculus operations.

</div>

---

## 💻 Installation

### Option 1: Quick Install (Recommended) ⭐

```bash
# 1. Create project folder
mkdir calculus-solver
cd calculus-solver

# 2. Ensure you have these files:
#    - math_solver.py
#    - requirements.txt
#    - README.md

# 3. Create virtual environment
python -m venv venv              # Windows/Mac
python3 -m venv venv             # Linux

# 4. Activate virtual environment
venv\Scripts\activate            # Windows
source venv/bin/activate         # Linux/Mac

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run application
python math_solver.py            # Windows/Mac
python3 math_solver.py           # Linux
```

### Option 2: Direct Install

```bash
pip install -r requirements.txt
python math_solver.py
```

> ⚠️ **Note:** Virtual environments are recommended for clean Python package management.

### System Requirements

| Component | Requirement |
|-----------|-------------|
| 🐍 Python | 3.7 or higher |
| 💾 RAM | 512 MB minimum |
| 💽 Storage | 100 MB for dependencies |
| 🖥️ OS | Windows, Linux, macOS |
| 🎨 Graphics | Any standard display |

### Verify Installation

```bash
pip list
```

**Expected packages:** `sympy`, `numpy`, `matplotlib`, `scipy`, `pillow`

---

## 🔧 Virtual Environment Setup

### What is a Virtual Environment?

A virtual environment is an isolated Python workspace that prevents package conflicts between projects.

```
System Python: SymPy 1.10, NumPy 1.24
        ↓
Virtual Env 1: SymPy 1.12, NumPy 1.26 ← Our project
        ↓
Virtual Env 2: SymPy 1.11, NumPy 1.25 ← Different project
```

### Windows Setup (7 Steps)

<details>
<summary><strong>Click to expand Windows instructions</strong></summary>

1. **Open Command Prompt**
   - Press `Windows + R`
   - Type `cmd`
   - Press Enter

2. **Navigate to Project**
   ```bash
   cd C:\Users\YourName\Desktop\calculus-solver
   ```

3. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

4. **Activate Virtual Environment**
   ```bash
   venv\Scripts\activate
   ```
   You should see `(venv)` appear before your prompt.

5. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run Application**
   ```bash
   python math_solver.py
   ```

7. **Deactivate When Done**
   ```bash
   deactivate
   ```

</details>

### Linux/Debian/Ubuntu Setup (8 Steps)

<details>
<summary><strong>Click to expand Linux instructions</strong></summary>

1. **Open Terminal**
   - Press `Ctrl + Alt + T`
   - Or search for "Terminal"

2. **Navigate to Project**
   ```bash
   cd ~/calculus-solver
   ```

3. **Check Python Version**
   ```bash
   python3 --version
   ```

4. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   ```

5. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

6. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

7. **Run Application**
   ```bash
   python3 math_solver.py
   ```

8. **Deactivate When Done**
   ```bash
   deactivate
   ```

</details>

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `python: command not found` | Use `python3` instead of `python` |
| `pip is not installed` | Run `python3 -m pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'sympy'` | Activate venv and run `pip install -r requirements.txt` |
| `Permission denied` (Linux) | Run `chmod +x math_solver.py` |
| Application won't start | Check Python version is 3.7+ |

---

## ✨ Features

### 🎯 12+ Mathematical Operations with Detailed Step-by-Step Solutions

<div align="center">

| Operation | Description | Example |
|-----------|-------------|---------|
| 📈 **Derivative** | Calculates rate of change (1st, 2nd, 3rd order) with full rule breakdown | `d/dx(x³) = 3x²` |
| ∫ **Integral** | Definite and indefinite integration with technique identification | `∫x²dx = x³/3 + C` |
| 🎯 **Limit** | Evaluates limits, handles indeterminate forms with L'Hôpital's rule | `lim(x→0) sin(x)/x = 1` |
| 📊 **Series Expansion** | Taylor/Maclaurin series with term-by-term construction | `eˣ ≈ 1 + x + x²/2 + x³/6` |
| ✓ **Solve Equation** | Solves algebraic equations showing all methods tried | `x² - 4 = 0 → x = ±2` |
| 🔧 **Simplify** | Simplifies expressions with identity applications | `x + x + 2x = 4x` |
| 📦 **Factor** | Factorizes polynomials with pattern recognition | `x² - 1 = (x-1)(x+1)` |
| 📐 **Expand** | Expands expressions using distributive property | `(x+1)² = x² + 2x + 1` |
| ➗ **Partial Fractions** | Decomposes rational functions step-by-step | `1/(x²-1) = ½(x-1) - ½(x+1)` |
| 📍 **Critical Points** | Finds extrema with derivative analysis | Local max/min detection |
| 〰️ **Inflection Points** | Finds concavity changes with second derivative | Concavity analysis |
| 📉 **Plotting** | Visualize functions with interactive graphs | Function visualization |

</div>

### 🔬 NEW: Enhanced Step-by-Step Engine v3.0

> 💡 **What makes Version 3.0 different?** Every solution now includes comprehensive step-by-step breakdowns that show:

```
┌────────────────────────────────────────────────────────────────────┐
│  📋 DETAILED STEP-BY-STEP SOLUTION                                 │
└────────────────────────────────────────────────────────────────────┘

Problem: x**2 + 2*x + 1
Operation: Derivative

────────────────────────────────────────────────────────────────────────

┌──────────────────────────────────────────────────────────────────────┐
│  Step  1: 📋 Problem Statement                                      │
└──────────────────────────────────────────────────────────────────────┘

📖 Description:
   We need to find the derivative of the given function

📘 Formula:
   f(x) = x² + 2x + 1

➡️  Result:
   Find: d/dx[x² + 2x + 1]

═══════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────┐
│  Step  2: 🔍 Step 1: Define Parameters                              │
└──────────────────────────────────────────────────────────────────────┘

📖 Description:
   Setting up the differentiation parameters

🔢 Calculation:
   Variable: x
   Order of derivative: 1

➡️  Result:
   We will compute the first derivative

═══════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────┐
│  Step  3: 🔍 Step 2: Function Analysis                              │
└──────────────────────────────────────────────────────────────────────┘

📖 Description:
   Analyzing the mathematical structure of the function

📘 Formula:
   f(x) = x² + 2x + 1

➡️  Result:
   Function type: Polynomial (degree 2)

═══════════════════════════════════════════════════════════════════════

[... continues with each rule applied ...]

┌──────────────────────────────────────────────────────────────────────┐
│  Step  N: ✅ Final Step: Compute Result                             │
└──────────────────────────────────────────────────────────────────────┘

📖 Description:
   Combining all applied rules to get the final derivative

📘 Formula:
   d¹/dx¹[x² + 2x + 1]

🔢 Calculation:
   Rules applied: Power Rule, Sum Rule

➡️  Result:
   2*x + 2

═══════════════════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════════════════╗
║  ✅ Solution Complete                                                ║
╚══════════════════════════════════════════════════════════════════════╝

Total Steps: 8
Result: 2*x + 2
```

#### How the Step-by-Step Engine Works:

1. **📋 Problem Statement** - Clearly defines what needs to be solved
2. **🔍 Function Analysis** - Identifies the type of mathematical function
3. **📝 Rule Application** - Tries ALL applicable formulas and rules:
   - Power Rule, Product Rule, Quotient Rule, Chain Rule
   - Trigonometric, Exponential, Logarithmic derivatives
   - Integration techniques (substitution, parts, partial fractions)
   - Algebraic manipulation methods
4. **✅ Result Computation** - Combines all applied rules
5. **✓ Verification** - Confirms the answer is correct

---

## 📖 User Guide

### Application Interface

```
┌────────────────────────────────────────────────────────────┐
│  🧮 Advanced Calculus Solver Pro - Version 2.0            │
├────────────────────────────────────────────────────────────┤
│  Input Expression:  [____________________________]         │
│  Operation:         [Derivative ▼]                         │
│                                                            │
│  [🔍 Solve]  [🗑️ Clear]  [❓ Help]                        │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  Result:   f'(x) = 3x²                                    │
│                                                            │
│  [📋 Copy]  [💾 Export]                                    │
│                                                            │
│  Steps:                                                    │
│  1. Recognized: x³                                         │
│  2. Applied derivative rule: d/dx(xⁿ) = n·xⁿ⁻¹            │
│  3. Result: 3x²                                            │
├────────────────────────────────────────────────────────────┤
│  [📜 History]  [📊 Plots]  [⚙️ Settings]  [🚪 Exit]      │
└────────────────────────────────────────────────────────────┘
```

### Main Components

| Component | Description |
|-----------|-------------|
| 📝 **Input Field** | Type your mathematical expression |
| 📋 **Operation Dropdown** | Select calculation type |
| 🔍 **Solve Button** | Execute the operation |
| 🗑️ **Clear Button** | Reset input field |
| 📊 **Result Panel** | Displays calculated answer |
| 📜 **Steps Panel** | Shows detailed working |
| 📋 **Copy Button** | Copy result to clipboard |
| 💾 **Export Button** | Save to PDF, Markdown, or Text |
| 📜 **History Tab** | View previous calculations |
| 📊 **Plots Tab** | Visualize functions |

### How to Use

#### Basic Operation

1. Type expression in input field
2. Select operation from dropdown
3. Click **Solve**
4. View result and steps
5. Copy or export if needed

#### With Parameters

- **Derivatives:** Type expression, select order
- **Integrals:** Type expression and limits (if definite)
- **Series:** Type expression, select order and point
- **Solve:** Type equation (use `=` for equations)

#### Exporting Results

1. Click **Export** button
2. Choose format (PDF, Markdown, Text)
3. Select save location
4. File is saved! 📁

---

## 🔤 Syntax Reference

### Basic Symbols & Operators

| Symbol | Meaning | Example |
|:------:|---------|---------|
| `+` | Addition | `x + 2` |
| `-` | Subtraction | `x - 3` |
| `*` | Multiplication | `2*x` |
| `/` | Division | `x/2` |
| `**` | Power/Exponent | `x**2` |
| `^` | Alternative power | `x^3` |
| `()` | Grouping | `(x+1)**2` |

### Functions

| Function | Syntax | Example |
|----------|--------|---------|
| Sine | `sin(x)` | `sin(x)` |
| Cosine | `cos(x)` | `cos(x)` |
| Tangent | `tan(x)` | `tan(x)` |
| Exponential | `exp(x)` | `exp(x)` |
| Natural Log | `log(x)` | `log(x)` |
| Base 10 Log | `log10(x)` | `log10(x)` |
| Square Root | `sqrt(x)` | `sqrt(x)` |
| Absolute | `abs(x)` | `abs(x)` |
| Pi | `pi` | `2*pi*r` |
| Euler's number | `e` | `e**x` |

### Common Expression Examples

```python
x**2 + 2*x + 1          # Quadratic
sin(x)/x                # Trigonometric
exp(x) * cos(x)         # Combined
(x**2 - 1)/(x - 1)      # Rational
sqrt(1 - x**2)          # With square root
log(x) + 1/x            # Mixed
```

### 💡 Input Tips

> ✅ **DO:**
> - Use `*` for multiplication: `2*x`
> - Use `**` for power: `x**2`
> - Use parentheses for clarity: `(x+1)**2`
> - Use standard variables: `x`, `y`, `t`, `θ`
>
> ❌ **DON'T:**
> - Write `2x` (use `2*x`)
> - Write `x^2` (use `x**2`)
> - Forget closing parentheses

---

## 📝 Worked Examples

### Example 1: Basic Derivative

**Problem:** Find the derivative of f(x) = x³

```
Input:    x**3
Select:   Derivative
Result:   3*x**2
```

**Explanation:** Using power rule: d/dx(xⁿ) = n·xⁿ⁻¹

---

### Example 2: Second Derivative

**Problem:** Find the second derivative of f(x) = x⁴

```
Input:    x**4
Select:   Derivative (Order = 2)
Result:   12*x**2
```

**Working:**
- First derivative: 4x³
- Second derivative: 12x²

---

### Example 3: Solving Equation

**Problem:** Solve x² - 5x + 6 = 0

```
Input:    x**2 - 5*x + 6
Select:   Solve
Result:   x = 2 or x = 3
```

**Verification:**
- For x=2: 4 - 10 + 6 = 0 ✓
- For x=3: 9 - 15 + 6 = 0 ✓

---

### Example 4: Definite Integral

**Problem:** Calculate ∫₀² x² dx

```
Input:    x**2
Select:   Integral
Limits:   From 0 to 2
Result:   8/3 or 2.667
```

**Working:** [x³/3]₀² = 8/3 - 0 = 8/3

---

### Example 5: Taylor Series

**Problem:** Expand eˣ around x=0 to 3rd order

```
Input:    exp(x)
Select:   Series Expansion
Point:    0
Order:    3
Result:   1 + x + x**2/2 + x**3/6
```

**Use:** For approximation when x is small

---

### Example 6: Limit Calculation

**Problem:** Find lim(x→0) sin(x)/x

```
Input:    sin(x)/x
Select:   Limit
Point:    0
Result:   1
```

> 📌 **Note:** This is undefined algebraically but the limit exists!

---

### Example 7: Simplification

**Problem:** Simplify (x²-1)/(x-1)

```
Input:    (x**2 - 1)/(x - 1)
Select:   Simplify
Result:   x + 1
```

**Explanation:** Factor numerator: (x-1)(x+1), cancel (x-1)

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Enter` | 🔍 Solve |
| `Ctrl + L` | 🗑️ Clear input |
| `Ctrl + C` | 📋 Copy result |
| `Ctrl + S` | 💾 Save/Export |
| `Ctrl + H` | 📜 Show history |
| `Ctrl + P` | 📊 Show plot |
| `Ctrl + ?` | ❓ Show help |
| `Escape` | Close current tab |

---

## 🔧 Troubleshooting

### Installation Issues

| Problem | Solution |
|---------|----------|
| `pip is not installed` | Run `python -m pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'sympy'` | 1. Activate venv<br>2. Run `pip install -r requirements.txt`<br>3. Verify: `pip list` |
| `Python version too old` | Install Python 3.7+ from [python.org](https://python.org) |

### Runtime Issues

| Problem | Solution |
|---------|----------|
| Application won't open | 1. Check Python: `python --version`<br>2. Check deps: `pip list`<br>3. Run with errors visible |
| Calculation too slow | 1. Simplify expression<br>2. Use smaller limits<br>3. Reduce series order |
| `Invalid expression` error | 1. Use `x**2` not `x^2`<br>2. Use `2*x` not `2x`<br>3. Match parentheses<br>4. Check function names |

### Usage Issues

| Problem | Solution |
|---------|----------|
| Can't calculate complex derivative | 1. Try simpler parts<br>2. Some expressions lack closed-form<br>3. Check syntax |
| Plot not showing | 1. Click Plots tab<br>2. Restart application<br>3. Ensure real-valued function |

---

## ❓ FAQ

<details>
<summary><strong>Q: Can I use this for calculus homework?</strong></summary>
<p>Yes! Perfect for checking answers. Remember to show your work separately.</p>
</details>

<details>
<summary><strong>Q: Is there a limit to expression complexity?</strong></summary>
<p>No hard limit, but very complex expressions may take longer to compute.</p>
</details>

<details>
<summary><strong>Q: Can I use different variables?</strong></summary>
<p>Yes! Use x, y, z, t, etc. The application detects them automatically.</p>
</details>

<details>
<summary><strong>Q: What if I make a mistake in input?</strong></summary>
<p>Click <strong>Clear</strong> or press <code>Ctrl+L</code> to start over.</p>
</details>

<details>
<summary><strong>Q: How do I save my work?</strong></summary>
<p>Click <strong>Export</strong> and choose format (PDF, Markdown, or Text).</p>
</details>

<details>
<summary><strong>Q: Can I use this offline?</strong></summary>
<p>Yes! No internet required once installed.</p>
</details>

<details>
<summary><strong>Q: Is my data private?</strong></summary>
<p>Yes! All calculations happen locally on your computer.</p>
</details>

<details>
<summary><strong>Q: Can I extend it with my own functions?</strong></summary>
<p>Yes! Edit <code>math_solver.py</code> to add custom operations.</p>
</details>

---

## 📦 Dependencies

This application uses powerful Python libraries:

| Library | Version | Purpose |
|---------|---------|---------|
| 🔢 **SymPy** | 1.12 | Symbolic mathematics |
| 📊 **NumPy** | 1.26.2 | Numerical computing |
| 📈 **Matplotlib** | 3.8.2 | Plotting/visualization |
| 🔬 **SciPy** | 1.11.4 | Scientific computing |
| 🖼️ **Pillow** | 10.1.0 | Image handling |

**Install all at once:**
```bash
pip install -r requirements.txt
```

---

## 🎯 Tips & Best Practices

### For Better Results

✅ **Simplify First**
- Complex expressions take longer
- Break into smaller parts

✅ **Use Clear Notation**
- `2*x` not `2x`
- `x**2` not `x^2`
- Use parentheses: `(x+1)**2`

✅ **Check Syntax**
- Verify function names: `sin`, `cos`, `tan`
- Verify operators: `*`, `/`, `**`, `()`
- Match all parentheses

✅ **Keep History**
- Review previous calculations
- Export interesting results
- Build a reference library

### Best Practices Workflow

1. Test on simple expressions first
2. Use `Tab` key to switch between fields
3. Copy and modify previous calculations
4. Export work regularly
5. Keep notes alongside calculations
6. Verify results make mathematical sense

---

## 🎓 Learning Resources

### Mathematics
- 📚 [Khan Academy Calculus](https://khanacademy.org/math/calculus-1)
- 🎥 [3Blue1Brown - Essence of Calculus](https://youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr)
- 📹 [PatrickJMT Calculus Videos](https://youtube.com/user/patrickJMT)

### Python & Libraries
- 🐍 [Python Official Documentation](https://docs.python.org)
- 🔢 [SymPy Documentation](https://docs.sympy.org)
- 📊 [NumPy Tutorial](https://numpy.org/devdocs/user/absolute_beginners.html)

### Virtual Environments
- 📖 [Python venv Guide](https://docs.python.org/3/library/venv.html)
- 💡 [Virtual Environment Best Practices](https://realpython.com/python-virtual-environments-a-primer/)

---

## 📞 Support & Issues

### Reporting Issues

If you encounter problems:

1. ✅ Check the **Troubleshooting** section above
2. ✅ Verify Python version: `python --version`
3. ✅ Verify dependencies: `pip list`
4. ✅ Check syntax of your expression
5. ✅ Try simpler expressions first

### Quick Fixes

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check SymPy installation
python -c "import sympy; print(sympy.__version__)"

# Verify virtual environment packages
pip list | grep -E "sympy|numpy|matplotlib"
```

---

## 📄 License & Credits

### Advanced Calculus Solver Pro - Version 2.0

*A professional mathematical computation tool*

**Built with:**
- 🐍 Python 3.7+
- 🔢 SymPy for symbolic mathematics
- 📊 NumPy for numerical operations
- 📈 Matplotlib for visualization
- 🔬 SciPy for scientific computing

---

## 🎊 You're Ready!

### What You Have Now

| ✅ | Item |
|----|------|
| ✔️ | Complete application |
| ✔️ | Full documentation |
| ✔️ | Setup instructions |
| ✔️ | Worked examples |
| ✔️ | Troubleshooting guide |
| ✔️ | Reference materials |

### Next Steps

1. 📥 Follow the **Installation Guide**
2. 🚀 Complete the **Quick Start**
3. 📝 Try the **Worked Examples**
4. 🔬 Explore all **12+ operations**
5. 💾 Export and save your work

---

<p align="center">
  <strong>Happy Solving!</strong> 🐍 ✨ 🧮 🎓
</p>

<p align="center">
  <em>Version 2.0 - Enhanced Edition | December 28, 2025</em>
</p>

<p align="center">
  <strong>Professional mathematical computing made simple.</strong>
</p>
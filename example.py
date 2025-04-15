import numpy as np
from sympy import symbols, plot
from scipy.interpolate import CubicSpline
from shumaker_spline import shumaker_spline

# Create symbolic variable for plotting
x_sym = symbols('x')

# --- Example 1: Simple Monotonic Data ---
print("--- Generating Plot 1: Simple Monotonic Data ---")
x1 = np.array([0, 1, 3, 4, 6])
y1 = np.array([0, 0.5, 0.6, 1.0, 1.1]) # Simple increasing data

# Calculate Shumaker spline (Sympy version)
spline1 = shumaker_spline(x1, y1, return_type='sympy')
print("Shumaker Spline (Example 1):")
print(spline1)
print("-" * 30)

# Plot only the data and the Shumaker spline with a clean label
p1 = plot((spline1, (x_sym, x1.min(), x1.max()), "Shumaker Spline"), # Explicit label
          show=False, title="Example 1: Simple Monotonic Data",
          markers=[{'args': [x1, y1, 'bo'], 'label': 'Data Points'}],
          legend=True, xlabel='x', ylabel='f(x)')
p1.show() # Display plot 1

# --- Example 2: Showing the Knots ---
print("\n--- Generating Plot 2: Showing Knots ---")
# Use the same data as Example 1
knots2, _ = shumaker_spline(x1, y1, return_type='coeffs') # Get knots
spline2 = spline1 # Reuse spline from Example 1
# No need to recalculate or reprint the spline if data is identical

# Plot data, spline (with label), and all knots
p2 = plot((spline2, (x_sym, x1.min(), x1.max()), "Shumaker Spline"), # Explicit label
          show=False, title="Example 2: Showing Knots",
          markers=[{'args': [knots2, [spline2.subs(x_sym, k) for k in knots2], 'go'], 'label': 'Shumaker Knots'},
                   {'args': [x1, y1, 'bo'], 'label': 'Data Points'}],
          legend=True, xlabel='x', ylabel='f(x)')
p2.show() # Display plot 2

# --- Example 3: Challenging Data - Comparison with Cubic ---
print("\n--- Generating Plot 3: Challenging Data & Comparison ---")
# New dataset designed to show cubic overshoot/oscillation
x3 = np.array([0, 1, 2, 3, 4, 5, 6])
y3 = np.array([0, 0.1, 0.2, 0.15, 1.5, 1.6, 1.55]) # Gradual start, sharp jump, then slight decrease

# Calculate Shumaker spline and knots
knots3, _ = shumaker_spline(x3, y3, return_type='coeffs')
spline_shumaker3 = shumaker_spline(x3, y3, return_type='sympy')
print("Shumaker Spline (Example 3):")
print(spline_shumaker3)
print("-" * 30)


# Calculate standard Cubic Spline
cs3 = CubicSpline(x3, y3)

# Plot data, Shumaker vs Cubic
p3 = plot((spline_shumaker3, (x_sym, x3.min(), x3.max()), 'Shumaker'),
          (cs3, (x_sym, x3.min(), x3.max()), 'Cubic (Scipy)'),
          show=False, title="Example 3: Comparison on Challenging Data",
          markers=[{'args': [x3, y3, 'bo'], 'label': 'Data Points'}],
          legend=True, xlabel='x', ylabel='f(x)')

p3.show()

print("\nDone generating examples.")
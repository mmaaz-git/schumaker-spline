import numpy as np
from sympy import symbols, Piecewise

def schumaker_spline(x, y, s = None, return_type = 'coeffs'):
    """
    Schumaker spline interpolation

    The Schumaker spline is a quadratic spline that is co-monotone and co-convex with the data.

    Args:
        x: array of x-coordinates, in ascending order
        y: array of y-coordinates, corresponding to x
        s: array of slopes, optional
        return_type: 'coeffs' or 'sympy', default is 'coeffs', if 'sympy', return a Sympy piecewise expression

    Returns:
        array of coefficients for the Shumaker spline with corresponding x-coordinates, or a Sympy piecewise expression
    """
    x, y = np.array(x), np.array(y)
    n = len(x)
    assert len(y) == n, "x and y must have the same length"
    assert np.all(np.diff(x) > 0), "x must be in ascending order"
    if s is not None:
        s = np.array(s)
        assert len(s) == n, "s must have the same length as x and y"

    # if not given, estimate the slopes at the data points
    if s is None:
        L = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
        delta =  np.diff(y) / np.diff(x)
        s = np.zeros(n)
        for i in range(1, n-1):
            if delta[i-1] * delta[i] > 0:
                s[i] = (L[i-1] * delta[i-1] + L[i] * delta[i]) / (L[i-1] + L[i])
            else:
                s[i] = 0
        s[0] = (3*delta[0] - s[1]) / 2
        s[n-1] = (3*delta[n-2] - s[n-2]) / 2

    # now loop over each interval and compute the knot and the quadratic spline(s)
    knots, coeffs = [], []
    for i in range(n-1):
        knots.append(x[i])

        # check if lemma is satisfied
        if (s[i] + s[i+1]) / 2 == (y[i+1] - y[i]) / (x[i+1] - x[i]):
            coeffs.append([y[i], # (x-x_i)^0 term
                           s[i], # (x-x_i)^1 term
                           (s[i+1] - s[i]) / (2 * (x[i+1] - x[i]))]) # (x-x_i)^2 term
        else:
            # have to add a new knot, depends on delta conditions
            if (s[i] - delta[i]) * (s[i+1] - delta[i]) >= 0:
                e = (x[i] + x[i+1]) / 2
            elif abs(s[i+1] - delta[i]) < abs(s[i] - delta[i]):
                e_temp = x[i] + 2*(x[i+1] - x[i])*(s[i+1] - delta[i]) / (s[i+1] - s[i])
                e = (x[i] + e_temp) / 2
            else:
                e_temp = x[i+1] + 2*(x[i+1] - x[i])*(s[i] - delta[i]) / (s[i+1] - s[i])
                e = (x[i+1] + e_temp) / 2

            knots.append(e)

            # compute the coefficients of the two splines, x[i] to e and e to x[i+1]
            # need some helper expressions
            alpha = e - x[i]
            beta = x[i+1] - e
            s_bar = (2*(y[i+1] - y[i]) - (alpha*s[i] + beta*s[i+1])) / (x[i+1] - x[i])
            A1 = y[i]
            B1 = s[i]
            C1 = (s_bar - s[i]) / (2 * alpha)
            A2 = A1 + alpha * B1 + alpha**2 * C1
            B2 = s_bar
            C2 = (s[i+1] - s_bar) / (2 * beta)
            # x[i] to e
            coeffs.append([A1,
                           B1,
                           C1])
            # e to x[i+1]
            coeffs.append([A2,
                           B2,
                           C2])

    knots.append(x[n-1])

    if return_type == 'coeffs':
        return np.array(knots), np.array(coeffs)
    elif return_type == 'sympy':
        x_sym = symbols('x')
        pieces = []
        for i in range(len(knots)-1):
            t = knots[i]
            a, b, c = coeffs[i]
            quadratic = a + b*(x_sym - t) + c*(x_sym - t)**2
            condition = (x_sym >= t) & (x_sym <= knots[i+1])
            pieces.append((quadratic, condition))
        return Piecewise(*pieces)
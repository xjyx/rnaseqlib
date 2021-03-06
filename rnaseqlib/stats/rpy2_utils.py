##
## Utilities related to Rpy2 library
##
import os
import sys
import time

import pandas
import numpy as np

import rnaseqlib
import rnaseqlib.utils as utils

try:
    import rpy2
    from rpy2.robjects import r
    import rpy2.robjects as robj
    import rpy2.robjects.numpy2ri
    from rpy2.robjects.packages import importr
    rpy2.robjects.numpy2ri.activate()
    from rpy2.robjects.lib import grid
    from rpy2.robjects import r, Formula
    py2ri_orig = rpy2.robjects.conversion.py2ri
except:
    print "WARNING: Cannot import rpy2"


def run_ma_loess(x, y, span=0.75):
    """
    Run MA-based loess normalization on X and Y. Computes

      M = log(X/Y)
      A = 0.5 * log(X*Y)

    Fits loess regression M ~ A and corrects X and Y accordingly.

    Assumes input X and Y values are non-logged.
    """
    M = np.log2(x) - np.log2(y)
    # A = average intensity 1/2(XY)
    A = 0.5 * (np.log2(x) + np.log2(y))
    # Fit M ~ A
    corrected_m, correction_factor = run_loess(A, M, span=span)
    corrected_x = 2**((2*A + corrected_m)/2.)
    corrected_y = 2**((2*A - corrected_m)/2.)
    return corrected_x, corrected_y


def where_na_like(l):
    """
    Return indices where array is NA-like
    """
    bool_index = np.array(map(lambda x: np.isinf(x) or \
                              pandas.isnull(x), l))
    return np.where(bool_index)[0]


def run_loess(x, y, span=0.75):
    """
    Predict y as function of x. Takes two numpy vectors.
    """
    # Ensure that Inf/-Inf values are substituted
    x[where_na_like(x)] = robj.NA_Real
    y[where_na_like(x)] = robj.NA_Real
    data = robj.DataFrame({"x": x, "y": y})
    loess_fit = r.loess("y ~ x", data=data, span=span,
                        family="symmetric")
    correction_factor = np.array(list(r.predict(loess_fit, x)))
    corrected_y = \
        np.array(list(y)) - correction_factor
    return corrected_y, correction_factor


def run_lowess(x, y, span=0.75):
    """
    Predict y as function of x. Takes two numpy vectors.

    Uses 'r.lowess' instead of 'r.loess'.
    """
    # Ensure that Inf/-Inf values are substituted
    x[where_na_like(x)] = robj.NA_Real
    y[where_na_like(x)] = robj.NA_Real
    data = robj.DataFrame({"x": x, "y": y})
    print "x: ", x, "y: ", y
    lowess_fit = r.lowess(data, f=span)
    print "LOWESS FIT: ", lowess_fit
    corrected_y = np.array(list(lowess_fit.y))
    return corrected_y, correction_factor



def main():
    pass
    #x = np.array([1, 0.5, 3, 4, 5, 5.5, 6, 7], dtype=np.float)
    #y = np.array([10, 25, 38, 44.5, 500, 550, 600, 705], dtype=np.float)
    #print "Results loess: ", run_loess(x, y)
    #print "Results LOWESS: ", run_lowess(x, y)
    


if __name__ == "__main__":
    main()

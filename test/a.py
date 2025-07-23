import numpy as np
import matplotlib.colors as mcolors # Import for colors
import math
import itertools

# My modules
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from settings import CONFIGURATION



def test(*, a = None, b = None, c = None):
    if a:
        print("a passed")
    if b:
        print("b passed")
    if c:
        print("c passed")

test(b=3, c=4)

array = np.array([0,1,2,3,5,6,7,8,9,10,10])
value = np.quantile(array, 0.9, method='higher')
print(value)    

print(type(None)())
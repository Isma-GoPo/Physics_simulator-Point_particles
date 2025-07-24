import numpy as np
import matplotlib.colors as mcolors # Import for colors
import math
import itertools

# My modules
from src.space_plotting import print_animated_simulation_by_space # raise error

from src.settings.settings import CONFIGURATION # depends on sys



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

print(type(None)())
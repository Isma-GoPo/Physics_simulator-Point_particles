import numpy as np
import matplotlib.colors as mcolors # Import for colors
import math
import itertools

# My modules
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from settings import CONFIGURATION



colours = list(mcolors.TABLEAU_COLORS)
colour_switcher: int = 0
color_gen = itertools.cycle(colours)

print(next(color_gen))
print(next(color_gen))
a = lambda: next(color_gen)
print(a())
print(a())
print(a())
import numpy as np
import matplotlib.colors as mcolors # Import for colors
import math
import itertools

# My modules
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings import CONFIGURATION



class PlottingDot():
    colours = list(mcolors.TABLEAU_COLORS)
    colours_generator = itertools.cycle(colours)


    def __init__(self, 
                 colour: str | None = None,
                 mass: float = 1.0, 
                 size: float | None = None) -> None:
        """Init a 'PlottingDot' object

        Possitional-Keyword arguments:
        mass: [-] a mass-like property of the particle used for defining size (default 1)
        colour: a matplotlib-compatible colour string
        size: [-] the size the dot will have in the plotting (overwrites mass if declared) (default log10(mass))
        """
        self.mass: float = float(mass) 
        self.colour: str = str(colour) if colour in mcolors.TABLEAU_COLORS else PlottingDot.get_new_colour()
        self.size = float(size) if size is not None else PlottingDot.mass_to_size(self.mass) # Being mass 1 by default
    
    # --- METHODS ---        
    
    # --- RETURNING METHODS ---

    @classmethod
    def get_new_colour(cls) -> str:
        return next(cls.colours_generator)
        
    def __str__(self) -> str:
        class_name = self.__class__.__name__
        attributes = '\n'.join(f"  {key}: {value}" for key, value in self.__dict__.items())
        return f"<{class_name} object at {hex(id(self))}>\n{attributes}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        attributes = ', '.join(f"{key} = {repr(value)}" for key, value in self.__dict__.items())
        return f"{class_name}({attributes})"
    
    # --- STATIC METHODS ---
    
    @staticmethod
    def mass_to_size(mass: float) -> float:
        return math.log(mass, 10)
    
    @staticmethod
    def get_colours_list(len: int) -> list[str]:
        """Return a list of colours of length `len`"""
        return [PlottingDot.get_new_colour() for _ in range(len)]
    
    @staticmethod
    def get_plotting_size_list_from_masses(mass_list: list[float]) -> list[float]:
        """Return a list of plotting sizes from a list of 
        """
        size_array = np.array([PlottingDot.mass_to_size(mass) for mass in mass_list])
        exp = CONFIGURATION.plotting.dot_sizes.exponent_factor #type: ignore
        geometric_size = PlottingDot._normalise_sizes(size_array)**exp * CONFIGURATION.plotting.dot_sizes.difference**(1-exp) #type: ignore # Make something similar to the geometric mean (because area != proprotional mass)
        return list(geometric_size* CONFIGURATION.plotting.dot_sizes.size_per_difference + CONFIGURATION.plotting.dot_sizes.min) #type: ignore

    @staticmethod
    def _normalise_sizes(sizes: np.ndarray) -> np.ndarray:
        default_difference = CONFIGURATION.plotting.dot_sizes.difference # type: ignore
        max = np.max(sizes)
        min = np.min(sizes)
        difference = max - min
        if difference <= default_difference:
            return sizes-min
        else:
            relative = lambda size: (size-min)*default_difference/difference
            return np.vectorize(relative)(sizes)  # like map()
    
    # --- METHODS ---

    
if __name__ == "__main__":  
    a = PlottingDot()
    b = PlottingDot()
    for _ in range(11):
        print(PlottingDot.get_new_colour())
    print(PlottingDot.get_plotting_size_list_from_masses([1, 2, 3, 4]))

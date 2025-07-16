import numpy as np
import matplotlib.colors as mcolors # Import for colors
import math



class PlottingDot():
    colours = list(mcolors.TABLEAU_COLORS)
    colour_switcher: int = 0


    def __init__(self, 
                 colour: str | None = None,
                 weight: float = 1.0, 
                 size: float | None = None) -> None:
        """Init a 'PlottingDot' object

        Possitional-Keyword arguments:
        weight: [-] a mass-like property of the particle used for defining size (default 1)
        colour: a matplotlib-compatible colour string
        size: [-] the size the dot will have in the plotting (overwrites weight if declared) (default log10(mass))
        """
        self.weight: float = float(weight) 
        self.colour: str = str(colour) if colour in mcolors.TABLEAU_COLORS else PlottingDot.set_new_colour()
        self.size = float(size) if size is not None else PlottingDot.weight_to_size(self.weight)

    @classmethod
    def set_new_colour(cls) -> str:
        colour = cls.colours[cls.colour_switcher]
        cls.colour_switcher = (cls.colour_switcher + 1) % len(cls.colours) 
        return colour
    
    @staticmethod
    def weight_to_size(weight: float) -> float:
        return math.log(weight, 10)
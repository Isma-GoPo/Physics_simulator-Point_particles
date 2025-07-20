import numpy as np
import math
from .config_class import Config


class ConfigPlotting(Config):
    def __init__(self, plotting_config: Config) -> None:
        """Init a 'ConfigSimulation' object

        Possitional-Keyword arguments:
        - simulation_config: base Config object defining the simulation configuration
        """
        self = plotting_config

        # --- PLOTTING BASE CONSTANTS ---

        self.plotting_time: float | np.float64 = np.float64( self.plotting_time )
            # How much the plotting of the simulation last (in [s])
        
        self.refresh_rate: int = int( self.refresh_rate )
            # Recommended to make it so it plots 30 step every second
        self.do_repeat: bool = bool( self.do_repeat )
            # If True, the plotting will repeat the last frame when it ends

        # --- SIZES BASE CONSTANTS ---
        self.dot_size_min = np.float64( self.dot_sizes.min )
        self.dot_size_max = np.float64( self.dot_sizes.max )
        self.dot_size_difference = np.float64( self.dot_sizes.difference )
        self.dot_sizes_exponent_factor = np.float64( self.dot_sizes.exponent_factor )





    # --- PLOTTING DERIVED CONSTANTS ---
    
    @property
    def number_of_plotting_steps(self) -> int:
        """How many plotting steps will be done in the simulation"""
        return int(self.plotting_time * self.refresh_rate)
    
    
    def plotting_relative_time_step(self, number_of_time_steps: int) -> int:
        return int(math.ceil(number_of_time_steps / (self.plotting_time * self.refresh_rate))) 
        

    # --- SIZES DERIVED CONSTANTS ---
    @property
    def size_per_difference(self) -> float | np.float64:
        return (self.size_max - self.size_min)/self.size_difference
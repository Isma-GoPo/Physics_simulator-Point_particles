# General modules
import numpy as np
from icecream import ic
from typing import Callable, Any

# My modules
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
# Relative imports
from functions import *
from constants import *
import physics as physics
from plotting import print_simulation_animated

# TESTING PURPOSES



# Running the file
if __name__=="__main__":
    particle = physics.Particle(1.0, initial_velocity = np.array([1.0,0.0,0.0]), acceleration_field = physics.GRAVITY)
    print(particle)
    particle.advance_time_step(TIME_STEP)
    particle.advance_time_step(TIME_STEP)
    print(particle.position_history)
    
    
    
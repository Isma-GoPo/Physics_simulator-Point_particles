# General modules
import numpy as np
from icecream import ic

# My modules
from functions import *
from constants import *
import physics

# Here is where the main program goes. It should be documented and organised by modules

# Running the file
if __name__=="__main__":
    gravity = np.array([0.0, 0.0, -9.81])  # Gravity vector in m/s^2 
    # make it a constant!!!
    # Make that it is always in the store_current_state() (it always applies gravity)
    particle = physics.Particle(1.0, acceleration_field = gravity)
    print(particle)
    particle.advance_time_step(1.0)  # Advance one second
    print(particle)
    particle.advance_time_step(1.0)  # Advance another second   
    print(particle)
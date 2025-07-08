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


    particle = physics.Particle(1.0, acceleration_field = physics.GRAVITY)
    
    positions = np.empty((0, 3), float)
    for _ in range(NUMBER_OF_TIME_STEPS):
        positions = np.vstack((positions, [particle.position]))
        particle.advance_time_step(TIME_STEP)
    print(f"Positions after 20 time steps: {positions}")
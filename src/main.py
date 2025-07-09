# General modules
import numpy as np
from icecream import ic

# My modules
#from functions import *
from constants import *
import utils
import physics
from plotting import print_simulation_animated

def define_simulation_setup() -> physics.ParticleSpace:
    """Define the simulation setup with particles."""
    space = physics.ParticleSpace()
    space.append(utils.init.free_falling_particle())
    space.append(utils.init.free_falling_particle(np.array([1.0, 0.0, 200.0])))
    return space    

# Running the file
if __name__=="__main__":
    space = define_simulation_setup()
    print(space)
    print(repr(space))

    space.run_simulation(NUMBER_OF_TIME_STEPS, TIME_STEP)
    
    
    
    
# General modules
import numpy as np
from icecream import ic

# My modules
#from functions import *
from constants import *
import utils
import physics
from plotting import print_simulation_animated

def define_test_simulation_space() -> physics.ParticleSpace:
    """Define the simulation setup with particles."""
    space = physics.ParticleSpace()
    space.append(utils.init.free_falling_particle())
    space.append(utils.init.free_falling_particle(np.array([1.0, 0.0, 2.0])))
    return space    

# Running the file
if __name__=="__main__":
    space = utils.init.orbiting_particles()
    print(space)
    #print(repr(space))
    
    def test_particle_function(particle: physics.Particle) -> None:
        """A test function to apply to each particle."""
        particle.apply_force(np.array([-0.2, 0.0, 0.0]))
        #print(particle)

    space.run_simulation(NUMBER_OF_TIME_STEPS, 
                         TIME_STEP, 
                         own_dynamic_operation_array=(),
                         couple_dynamic_operation_array=(physics.dynamics.couple.gravitational_force,))
    
    
    
    
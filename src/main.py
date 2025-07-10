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
    space.append(utils.init.free_falling_particle(np.array([1.0, 0.0, 2.0])))
    return space    

# Running the file
if __name__=="__main__":
    space = define_simulation_setup()
    print(space)
    print(repr(space))
    
    def test_particle_function(particle: physics.Particle) -> None:
        """A test function to apply to each particle."""
        particle.apply_force(np.array([-0.2, 0.0, 0.0]))
        #print(particle)
    
    def test_attraction_function(particle1: physics.Particle, particle2: physics.Particle) -> None:
        """A test function to apply to each particle."""
        distance = np.linalg.norm(particle1.position - particle2.position)
        force_mod = 1/distance**2 if distance != 0 else 0
        force_dir: np.ndarray = (particle1.position - particle2.position)/distance 
        force: np.ndarray = force_mod * force_dir

        particle1.apply_force(force)
        particle2.apply_force(-force)
        #print(particle)

    space.run_simulation(NUMBER_OF_TIME_STEPS, TIME_STEP, (test_particle_function,), (test_attraction_function,))
    
    
    
    
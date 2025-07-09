# General modules
import numpy as np
from icecream import ic

# My modules
from functions import *
from constants import *
import physics
from plotting import print_simulation_animated

# Here is where the main program goes. It should be documented and organised by modules
def run_simulation() -> np.ndarray:
    """Run the simulation of a particle under the influence of gravity."""
    particle = physics.Particle(1.0, initial_velocity = np.array([1.0,0.0,0.0]), acceleration_field = physics.GRAVITY)
    print(particle)
    # Initialize an empty array to store positions
    positions = np.empty((0, 3), float)

    # Advance the particle through time steps
    for _ in range(NUMBER_OF_TIME_STEPS):
        positions = np.vstack(tup=(positions, [particle.position]))
        particle.advance_time_step(TIME_STEP)

    return positions.copy()
    

# Running the file
if __name__=="__main__":
    position1 = run_simulation()
    position2 = run_simulation()*2
    #print(f"Positions after {NUMBER_OF_TIME_STEPS} time steps:\n{position1}")
    #print_simulation_animated_one_particle(position1)
    print_simulation_animated(position1, position1+1, position2)
    #print(NUMBER_OF_TIME_STEPS)
    
    
    
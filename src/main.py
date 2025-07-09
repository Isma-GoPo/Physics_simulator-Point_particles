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

    # Initialize an empty array to store positions
    positions = np.empty((0, 3), float)

    # Advance the particle through time steps
    for _ in range(NUMBER_OF_TIME_STEPS):
        positions = np.vstack((positions, [particle.position]))
        particle.advance_time_step(TIME_STEP)

    return positions
    

# Running the file
if __name__=="__main__":
    positions = run_simulation()
    print(f"Positions after {NUMBER_OF_TIME_STEPS} time steps:\n{positions}")
    print_simulation_animated(positions)
    print(NUMBER_OF_TIME_STEPS)
    
    
    
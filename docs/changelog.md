This is the log file. Its purpose is to have an idea of what I have done when I enter the project a long time later.

## v0.3 [2025-07-14]
###### Summary
Better physics package with ParticleSpace class, dynamic>force functions, and quick default space initializers

###### Detailed changes
- Updated the Particle class
  - Include a position history and privatized certain properties.
  - updated apply_acceleration method workings for more accurate results
- ParticleSpace class added for managing large collections of particles and simulating them
  - Added position_history_array property to ParticleSpace
  - Able to contain forces to operate with during the simulation
- Added dynamics package for managing dynamics/physical operations for the particles: couple and single forces. 
  - Added gravitational, viscosity force, and other cinematic forces to play with. 
  - Added limit_force decorator
  - deprecated "dynamic_operations" for just forces that get applied in ParticleSpace
- Introduced an `init_particle` and `init_space` module in the utils package for creating default particles and spaces (runs quickly)
  - gravitational orbit, circular motion, free-falling particles, etc.

## v0.2 [2025-07-08]
Adding the necessary modules and functions for plotting and animating the positions of the simulated particles.

## v0.1 [2025-07-08]
Adding the Particle class and its basic methods.

## v0.0 [2025-07-08]
Starting the project.
###### Documentation
I wrote the basic documentation for the project.
###### Github
I initialised a repo on GitHub for learning how to use it.
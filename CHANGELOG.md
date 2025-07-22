This is the log file. Its purpose is to have an idea of what I have done when I enter the project a long time later.

## v0.7 
...

Made Dot to plotting class independent of the particles itselfs

## v0.6 [2025-07-22]
###### Summary
Constants of the simulation or plotting are now managed by `settings` module, mainly by `Config` class and its subclasses. That inherit from a new `NestedHash` class.

###### NestedHash
- It is a class which allow managing nested dicts with several properties that make it usefull for using it as config objects.
  - Allow updating all its values with a dict, forcing the type of the old value and checking for not deleting nested structures

###### Config
- Itoduced a general `Config` class in `settings` that acts as a constant for the default simulation and plotting configuration. 
  - For it, the module initialize `CONFIGURATION = Config()` constant
  - Is intented to be used as a unique instance in the program.
- It is set up from `ConfigSimulation`, `ConfigPlotting`, `ConfigSizes` classes (also inherit from `NestedHash`)

## v0.5 [2025-07-20]
###### Summary
Upgraded the pyhisics module so now its support adaptative simulation and has life_time property. Added a solar system init space. 


###### Adaptative simulation
- Make a particle/space detect when the acceleration (increase in velocity for an step) is too big (defined by configuration) so it split the steps in two recursively
  - Make every iteration check the velocity_diff and split the steps only if necessary.
- Then merge all this steps in just one position_history (so plotting and future features are easier)

###### Other changes
- Added to Particle and ParticleSpace its `live time span`
  - This allow time-depending functions
- Deleted unused extra single_forces_array and couple_forces_array (not in self arrays)

## v0.4 [2025-07-16]
Organaising repo: adding roadmap, license; deleting unused modules and __pycache__.
Added functional setting.yalm for configuring the simulation and plotting


## v0.3 [2025-07-14]
###### Summary
Better physics package with ParticleSpace class, dynamic>force functions, and quick default space initializers

###### Detailed changes of physics package
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

###### Other changes
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
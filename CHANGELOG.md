This is the log file. Its purpose is to have an idea of what I have done when I enter the project a long time later.


## v0.7.2 [2025-07-XX]
...
- In adaptManager if setp< min try to check and if it fails is when `min_time_step_failed` should works instead of `do_last_time_failed`
- Make that store_value in adaptability manager works when is not adaptative

## v0.7.1 [2025-07-27]
Quality of life improvements:
- Solved bugs
- Updated documentation inside code for all modules and packages 
- Refactoring AdaptabilityManager code and solving a bug with adaptability
  - Privatised last_threshold_absolute_value and only return it when do_last_failed is true, if not raise error
  - Refactored `check_ok` for returning True or making changes, but not both
- corrected some Particle and Space methods and properties

## v0.7 [2025-07-26]
###### Summary
Adaptability in the simulation has been improved and added complexity and options. This possibility make the particle slower but more powerfull for being precise in extreme situations that needs more time steps.

###### AdaptabilityManager
- `AdaptabilityManager` is a class that is contained in each particle that allow managing the adaptative steps.
- For the user they add:
  - Different thresholds values and functions: for a given max_absolute_value, percentile (extrapolated to >1), standard deviation
  - `check_adaptative_ok` method for ckecking if the a magnituede (now the velocity differential) with all the different thresholds.
  - `self.recommended_division_for_steps` for setting the adaptative steps
  - Make so `AdaptabilityManager` returns also the number of time steps you should divide into for quickler results
- Made it independand of the atribute (`velocity_diff`) 
  - It takes whatever function of the particle for setting the adaptability ckecking
  - Add a this atribute history for statistic/relative thresholds
- When min_time_step is reached, it takes the max threshold computed value
- The most reccomended feature is `max_quantile = 1.5~4.` toguether with `quantile_ignored_extremes = 10~1`

###### Other changes
- New `AdaptabilityConfig` class as part of `Config > ConfigSimulation`
- Made `Dot` to plotting class independent of the particles itselfs
- Added default config for init `orbiting_decelerating_particles` and creating `two_particles_from_repose` as setting for experimenting with adaptative simulation

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
# Roadmap
This is the roadmap of this repository. The features I want to be adding in a future.

## More functions and init spaces
- Add more functions

### Live time span
- Add to Particle its `live time span`
  - This allow time-depending functionsw

## Charge particle
- Add a Particle subClass with charge
  - Add electric forces functions

## Adaptative iterations
- Make a particle/space detect when the acceleration (increase in velocity for an step) is too big (@constant) so it split the steps in two
  - or split them in `ceil(current_velocity_diff / Constant.max )`
- Make every iteration check the velocity_diff and split the steps only if necessary.
- Then merge all this steps in one (so plotting and all things are easier)



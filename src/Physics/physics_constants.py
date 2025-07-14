"""This module contains all physics constants necessary to apply the interations between particles

Constatns:
GRAVITY: [m/s^2] the gravity vector in Earth
"""
import numpy as np

# Numeric constatants
GRAVITATIONAL_CONSTANT = np.float64(6.67430e-11)  # [m^3 kg^-1 s^-2] Gravitational constant

# Field constants

GRAVITY_FIELD = np.array([0.0, 0.0, -9.81])

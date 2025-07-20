from .settings import *
from .config_simulation import ConfigSimulation
from .config_plotting import ConfigPlotting

USER_CONFIGURATION: Config = DEFAULT_CONFIGURATION.copy()
USER_CONFIGURATION.update(USER_SETTINGS_DICT)
USER_CONFIGURATION.simulation = ConfigSimulation(USER_CONFIGURATION.simulation)
USER_CONFIGURATION.plotting = ConfigPlotting(USER_CONFIGURATION.plotting)

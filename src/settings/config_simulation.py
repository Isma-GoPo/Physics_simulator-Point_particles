import numpy as np

# My modules
from .config_class import Config


class ConfigSimulation(Config):
    def __init__(self, simulation_config: Config) -> None:
        """Init a 'ConfigSimulation' object

        Possitional-Keyword arguments:
        - simulation_config: base Config object defining the simulation configuration
        """
        self = simulation_config

        self.max_allowed_force: float | np.float64 = np.float64( self.max_allowed_force )
        # Maximum force module (norm) that can be applied to a particle (in [N]) `np.inf` means no limit

        # --- SIMULATION TIME CONSTANTS ---
        self.time_step: float | np.float64 = np.float64( self.time_step )
            # How much it "tick" advance the time in the simulation (in [s])
            # 0.001 slow but really accurate
        self.simulation_time: float | np.float64 = np.float64( self.simulation_time )
            # How much the simulation last (in [s])

        # --- SIMULATION ADAPTATIVE ---
        self.is_adaptative: bool = bool( self.is_adaptative )
            # If True, the simulation will be adaptative
        self.max_velocity_diff: float | np.float64 = np.float64( self.max_velocity_diff )
            # defines the the adapatative accuracy
    
    @property
    def number_of_time_steps(self) -> int:
        """How many time steps will be done in the simulation"""
        return int(self.simulation_time / self.time_step)
    
    def _could_crass(self) -> bool:
        could_crass = int(self.simulation_time / self.time_step) > 100_000

        return could_crass



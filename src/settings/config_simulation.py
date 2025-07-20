from settings.settings import SETTINGS
import numpy as np


class ConfigSimulation:
    def __init__(self, config_file: str, config_dict: dict) -> None:
        """Init a 'ConfigSimulation' object

        Possitional-Keyword arguments:
        
        """
        self.MAX_FORCE_MODULE: float | np.float64 = np.float64( SETTINGS["simulation"]["max_allowed_force"] )
        # Maximum force module (norm) that can be applied to a particle (in [N]) `np.inf` means no limit

        # --- SIMULATION TIME CONSTANTS ---
        self.TIME_STEP: float | np.float64 = np.float64( SETTINGS["simulation"]["time_step"] )
            # How much it "tick" advance the time in the simulation (in [s])
            # 0.001 slow but really accurate
        self.SIMULATION_TIME: float | np.float64 = np.float64( SETTINGS["simulation"]["simulation_time"] )
            # How much the simulation last (in [s])
        self.NUMBER_OF_TIME_STEPS: int = int(self.SIMULATION_TIME / self.TIME_STEP)  
        if self.NUMBER_OF_TIME_STEPS > 100_000: raise Exception("Too many time steps could crash")
            # How many time steps will be done in the simulation

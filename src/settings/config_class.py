"""`config_class` module include the `Config` class"""

from types import SimpleNamespace
from typing import Any

class Config(SimpleNamespace):
    """
    A class to transform a dictionary (including nested dictionaries) into an object where keys are accessible as attributes
    Nested dictionaries are managed recursevely (as Config functions).
    """
    def __init__(self, dictionary: dict[str, Any], overwritter_dict: dict[str, Any] | None = None) -> None:
        """
        Initialize the Config object with a dictionary, overwritten the atributes given in over overwritter_dict

        Possitional-Keyword arguments:
        dictionary: the base dictionary for initialization
        overwritter_dict: an optional dictionary that will overwritte the Config atributes calling the update method
        """
        processed_dict = Config._processed_dict(dictionary)
        super().__init__(**processed_dict)
        if overwritter_dict is not None:
            self.update(overwritter_dict)


    @staticmethod
    def _processed_dict(unprocessed_dict: dict[str, Any]) -> dict[str, Any]:
        processed_dict = {}
        for key, value in unprocessed_dict.items():
            key = Config._sanitase_key(key)
            if isinstance(value, dict):
                # Recursively create another Config object for nested dictionaries
                value = Config(value)
            else:
                # Assign simple values directly
                pass
            processed_dict[key] = value
        return processed_dict
    
    @staticmethod
    def _sanitase_key(key: str) -> str:
        """Sanitize key if it's not a valid Python atribute name"""
        return key.replace("-", "_").replace(" ", "_")
    
    @property
    def as_dictionary(self) -> dict[str, Any]:
        dict = self.__dict__
        for key, value in dict.items():
            if isinstance(value, Config):
                dict[key] = value.as_dictionary
        return dict
    
    def __setattr__(self, key: str, new_value: Any) -> None:
        if isinstance(new_value, dict):
            return super().__setattr__(key, Config(new_value))
        return super().__setattr__(key, new_value)
    
    def update(self, new_dictionary: dict[str, Any]) -> None:
        """Update the object with a new dictionary. 
        If the value to overweite is a Config, it recursevely update it.
        If the new value is None, it does not overwrite."""
        for key, new_value in new_dictionary.items():
            if not hasattr(self, key):
                setattr(self, key, new_value)
            else:
                old_value = getattr(self, key)
                if new_value is None:
                    continue
                if isinstance(old_value, Config):
                    if isinstance(new_value, dict):
                        old_value.update(new_value)
                    else:
                        continue
                else:
                    setattr(self, key, new_value)

    
if __name__ == "__main__":
    obj = Config({"simulation_time": 40, "time": {"life": {"first": 1, "second": 2}, "death": 28}})
    print(obj)
    obj.update({"time": {"life": "AA"}})
    print(obj)
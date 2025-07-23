"""`nestedhash` module include the `NestedHash` class"""

from typing import Any
from copy import deepcopy

from icecream import ic


class NestedHash():
    """
    A class to transform a dictionary (including nested dictionaries) into an object where keys are accessible as attributes
    Nested dictionaries are managed recursevely (as NestedHash functions).
    """
    def __init__(self, 
                 dictionary: dict[str, Any] | None = None, 
                 overwritter_dict: dict[str, Any] | None = None) -> None:
        """
        Initialize the NestedHash object with a dictionary, overwritten the atributes given in over overwritter_dict

        Possitional-Keyword arguments:
        - dictionary: the base dictionary for initialization
        - overwritter_dict: an optional dictionary that will overwritte the NestedHash atributes calling the update method
        """
        dictionary = {} if dictionary is None else dictionary
        cls = self.__class__
        for key, value in dictionary.items():
            key = cls._sanitase_key(key)
            if isinstance(value, dict):
                setattr(self, key, cls(value))
            else:
                setattr(self, key, value)
        if overwritter_dict is not None:
            self.update(overwritter_dict)
    
    @staticmethod
    def _sanitase_key(key: str) -> str:
        """Sanitize key if it's not a valid Python atribute name"""
        return key.replace("-", "_").replace(" ", "_")
    
    @property
    def as_dictionary(self) -> dict[str, Any]:
        dict = self.__dict__
        for key, value in dict.items():
            if isinstance(value, NestedHash): # Also True if it is a subclass
                dict[key] = value.as_dictionary
        return dict
    
    @property
    def copy(self) -> Any:
        """Return a copy of the object"""
        return deepcopy(self)
    
    # --- Dunder methods ---

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        atributes = (f"{k}: {repr(v)}" for k, v in self.__dict__.items())
        return f"{class_name}({', '.join(atributes)})"

    #def __str__(self) -> str:
    #    return str(self.as_dictionary)

    def __eq__(self, other) -> bool | Any:
        cls = self.__class__
        if isinstance(self, cls) and isinstance(other, cls):
           return self.__dict__ == other.__dict__
        return NotImplemented
    
    def __setattr__(self, key: str, new_value: Any) -> None:
        cls = self.__class__
        if isinstance(new_value, dict):
            return super().__setattr__(key, cls(new_value))
        return super().__setattr__(key, new_value)
    
    def __delattr__(self, key: str) -> None:
        getattr(self, key)
        
    def __getitem__(self, key: str) -> dict[str, Any]:
        """getitem but allowing accessing nested keys by dot notation.
        
        Example: config["user1"]["ip"] == config["user1.ip"]"""
        if "." in key:
            keys = key.split(".")
            return self.get(*keys)
        # If no dotkey.
        return getattr(self, key)
    
    # --- Custom methods ---

    def get(self, key: str, *nested_keys: str) -> Any:
        try:
            if len(nested_keys) == 0:
                return getattr(self, key)
            elif len(nested_keys) >= 1:
                return getattr(self, key).get(*nested_keys)
        except:
            return None
    
    def update(self, new_dictionary: dict[str, Any]) -> None:
        """Update the object with a new dictionary, forcing the new type to be the old one. 
        If the value to overweite is a NestedHash, it recursevely update it.
        If the new value is None, it does not overwrite.
        
        It only supports objects of classes which are called by their class name. For example, it doesn't support `numpy.ndarray` because are called by `numpy.array`.
        """
        for key, new_value in new_dictionary.items():
            key = self._sanitase_key(key)
            if not hasattr(self, key):
                setattr(self, key, new_value)
            else:
                old_value = getattr(self, key)
                if new_value is None:
                    continue
                if isinstance(old_value, NestedHash):
                    if isinstance(new_value, dict):
                        old_value.update(new_value)
                    else:
                        continue
                else:
                    if old_value is None:
                        setattr(self, key, new_value)
                    else:
                        typeclass = type(old_value)
                        setattr(self, key, typeclass(new_value))
    
    

    
if __name__ == "__main__":

    import numpy as np
    obj = NestedHash({"simulation_time": 40, "time": {"life": {"first": 3.2, "second": 2}, "death": 28}})
    #print(repr(obj))
    obj.update({"time": {"life": {"first": 1}}})
    #print(obj.a) # type: ignore
    #print(obj["timelife.second"])

    obj2 = obj.copy
    obj2.update({"time": {"life": {"first": 5}}})
    print(obj)
    print(obj2)



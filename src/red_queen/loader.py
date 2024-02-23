import importlib
import logging

_LOGGER = logging.getLogger("red_queen.loader")


def _load_entry_point(entity_string):
    package_path, entity_name = entity_string.split(":")
    package = importlib.import_module(package_path)
    return getattr(package, entity_name)


def load_object(dictionary, **kwargs):
    """
    Loads a python object decribed from a json dictionary
    """
    _LOGGER.info("Loading python object: %s", str(dictionary))
    fun = _load_entry_point(dictionary["entry_point"])
    args = dictionary.get("args", [])
    kwargs.update(dictionary.get("kwargs", {}))
    if args or kwargs:
        return fun(*args, **kwargs)
    return fun

import streamlit as st
import importlib
import os


def _load_pimped_function(name):
    # Look for a corresponding file in the `elements` directory
    elements_path = os.path.join(os.path.dirname(__file__), "elements", f"{name}.py")
    if os.path.exists(elements_path):
        module_name = f"pimpmystreamlit.elements.{name}"
        module = importlib.import_module(module_name)
        return getattr(module, f"pimped_{name}", None)
    return None


def __getattr__(name):
    # Attempt to load a pimped function
    pimped_func = _load_pimped_function(name)
    if pimped_func:
        return pimped_func

    # Fall back to Streamlit
    if hasattr(st, name):
        return getattr(st, name)

    # Raise an error if neither exists
    raise AttributeError(f"Streamlit has no '{name}' element")

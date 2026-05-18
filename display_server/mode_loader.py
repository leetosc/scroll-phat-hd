import importlib.util
import os
import sys
import traceback

from .registry import EXAMPLES_DIR


def load_module(script_path, mode_id):
    """Load a script as a module with a stable name."""
    if EXAMPLES_DIR not in sys.path:
        sys.path.insert(0, EXAMPLES_DIR)

    module_name = "scrollphat_mode_{}".format(mode_id.replace("-", "_"))
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise ImportError("Cannot load {}".format(script_path))

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_mode(module, stop_event, get_config):
    if not hasattr(module, "run_display"):
        raise AttributeError("Script has no run_display() function")
    module.run_display(stop_event=stop_event, get_config=get_config)


def format_error(exc):
    return "".join(traceback.format_exception_only(type(exc), exc)).strip()

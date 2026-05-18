import os

from .schema import build_schema, discover_constants, mode_metadata

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES_DIR = os.path.join(REPO_ROOT, "examples")
DEFAULT_MODE = "clock4"
EXCLUDED = {"web-api"}


def _discover_modes():
    modes = {}

    clock4_path = os.path.join(REPO_ROOT, "clock4.py")
    constants = discover_constants(clock4_path)
    modes["clock4"] = {
        "id": "clock4",
        "label": "Clock (clock4)",
        "path": clock4_path,
        "defaults": constants,
        "schema": build_schema(constants),
        **mode_metadata("clock4"),
    }

    for filename in sorted(os.listdir(EXAMPLES_DIR)):
        if not filename.endswith(".py"):
            continue
        mode_id = filename[:-3]
        if mode_id in EXCLUDED:
            continue
        path = os.path.join(EXAMPLES_DIR, filename)
        if not os.path.isfile(path):
            continue
        constants = discover_constants(path)
        modes[mode_id] = {
            "id": mode_id,
            "label": mode_id.replace("-", " ").title(),
            "path": path,
            "defaults": constants,
            "schema": build_schema(constants),
            **mode_metadata(mode_id),
        }

    return modes


MODES = _discover_modes()


def list_modes():
    return [
        {
            "id": m["id"],
            "label": m["label"],
            "schema": m["schema"],
            "requires_deps": m.get("requires_deps", []),
            "note": m.get("note"),
        }
        for m in MODES.values()
    ]


def get_mode(mode_id):
    return MODES.get(mode_id)

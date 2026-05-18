import ast
import os


def _literal_value(node):
    try:
        return ast.literal_eval(node)
    except (ValueError, SyntaxError):
        return None


def discover_constants(script_path):
    """Return {NAME: default_value} for module-level UPPER_SNAKE assignments."""
    with open(script_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source, filename=script_path)
    constants = {}

    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        value = _literal_value(node.value)
        if value is None:
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id.isupper():
                constants[target.id] = value

    return constants


def infer_field_type(name, value):
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int) and not isinstance(value, bool):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        if "KEY" in name or "SECRET" in name or "TOKEN" in name:
            return "secret"
        return "str"
    return "str"


def build_schema(constants):
    """Build UI schema entries from constant defaults."""
    fields = []
    for name, default in sorted(constants.items()):
        field_type = infer_field_type(name, default)
        entry = {
            "name": name,
            "type": field_type,
            "default": default,
        }
        if field_type == "float":
            if any(x in name for x in ("BRIGHT", "DIM", "GUST", "WIND", "OPACITY")):
                entry["min"] = 0.0
                entry["max"] = 1.0
                entry["step"] = 0.01
            else:
                entry["step"] = 0.1
        elif field_type == "int":
            entry["step"] = 1
        fields.append(entry)
    return fields


MODE_HINTS = {
    "cpu": {"requires_deps": ["psutil"]},
    "cellular-automata": {"requires_deps": ["numpy"]},
    "twitter-hashtag": {"requires_deps": ["tweepy"], "note": "Requires Twitter API keys in config"},
    "openweather-temp-display": {"note": "Requires OpenWeather API key (OW_API_KEY)"},
    "hello-pigpiod": {"requires_deps": ["pigpio"], "note": "Requires pigpiod daemon"},
}


def mode_metadata(mode_id):
    return dict(MODE_HINTS.get(mode_id, {}))

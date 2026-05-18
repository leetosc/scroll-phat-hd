"""Shared helpers so display modes pick up web UI config after Apply."""

import json


def parse_lines(raw, default):
    """Parse line lists from config (list, JSON, newlines, or commas)."""
    if isinstance(raw, list):
        return [str(line) for line in raw if str(line).strip()]
    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            return list(default)
        if text.startswith("["):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, list):
                    return [str(line) for line in parsed if str(line).strip()]
            except (ValueError, TypeError):
                pass
        if "\n" in text:
            return [line.strip() for line in text.splitlines() if line.strip()]
        return [part.strip() for part in text.split(",") if part.strip()]
    return list(default)


def parse_int_list(raw, default):
    """Parse a list of integers from config."""
    if isinstance(raw, list):
        return [int(x) for x in raw]
    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            return list(default)
        if text.startswith("["):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, list):
                    return [int(x) for x in parsed]
            except (ValueError, TypeError):
                pass
        parts = text.replace(",", " ").split()
        return [int(x) for x in parts if x.strip()]
    return list(default)


def config_tuple(get_config, keys_defaults):
    return tuple(get_config(key, default) for key, default in keys_defaults)


def sync_scrolling_text(get_config, cache, text_key, text_default, brightness_key, brightness_default, **write_kwargs):
    """Redraw scroll buffer when text or brightness changes. Returns True if redrawn."""
    import scrollphathd

    text = get_config(text_key, text_default)
    brightness = get_config(brightness_key, brightness_default)
    extra = tuple(sorted(write_kwargs.items()))
    key = (text, brightness, extra)
    if cache.get("scroll_text") == key:
        return False
    scrollphathd.clear()
    scrollphathd.write_string(text, brightness=brightness, **dict(extra))
    cache["scroll_text"] = key
    return True


def sync_rotation(get_config, cache, key, default):
    """Apply rotation when degrees change. Returns True if changed."""
    import scrollphathd

    degrees = get_config(key, default)
    if cache.get(key) == degrees:
        return False
    scrollphathd.rotate(degrees=degrees)
    cache[key] = degrees
    return True

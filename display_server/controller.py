import threading

import scrollphathd

from .config_store import ConfigStore
from .mode_loader import format_error, load_module, run_mode
from .registry import DEFAULT_MODE, get_mode


class DisplayController:
    def __init__(self):
        self.store = ConfigStore()
        self._stop_event = threading.Event()
        self._thread = None
        self._error = None
        self._lock = threading.Lock()

    @property
    def error(self):
        with self._lock:
            return self._error

    def _clear_display(self):
        try:
            scrollphathd.clear()
            scrollphathd.show()
        except Exception:
            pass

    def _worker(self, mode_id, script_path):
        try:
            module = load_module(script_path, mode_id)
            run_mode(module, self._stop_event, self.store.make_getter())
        except Exception as exc:
            with self._lock:
                self._error = format_error(exc)
        finally:
            self._clear_display()

    def stop(self):
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
        self._thread = None
        self._stop_event = threading.Event()

    def set_mode(self, mode_id, defaults_only=False):
        mode = get_mode(mode_id)
        if mode is None:
            raise ValueError("Unknown mode: {}".format(mode_id))

        with self._lock:
            self._error = None

        self.stop()

        config = dict(mode["defaults"])
        if not defaults_only:
            current = self.store.get_config()
            if self.store.mode_id == mode_id and current:
                config.update(current)

        self.store.set_mode(mode_id, config)

        self._thread = threading.Thread(
            target=self._worker,
            args=(mode_id, mode["path"]),
            name="scrollphat-display",
            daemon=True,
        )
        self._thread.start()

    def reset_config(self):
        mode = get_mode(self.store.mode_id)
        if mode is None:
            return
        self.store.set_mode(mode["id"], dict(mode["defaults"]))

    def start_default(self):
        self.set_mode(DEFAULT_MODE, defaults_only=True)

    def state(self):
        return {
            "mode": self.store.mode_id,
            "config": self.store.get_config(),
            "error": self.error,
        }

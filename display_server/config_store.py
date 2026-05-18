import threading


class ConfigStore:
    """Thread-safe store for the active mode id and its parameter values."""

    def __init__(self):
        self._lock = threading.RLock()
        self._mode_id = None
        self._config = {}

    @property
    def mode_id(self):
        with self._lock:
            return self._mode_id

    def get_config(self):
        with self._lock:
            return dict(self._config)

    def get(self, key, default=None):
        with self._lock:
            return self._config.get(key, default)

    def set_mode(self, mode_id, config):
        with self._lock:
            self._mode_id = mode_id
            self._config = dict(config)

    def update(self, values):
        with self._lock:
            self._config.update(values)

    def make_getter(self):
        """Return a get_config callable for display loops."""

        def getter(key, default=None):
            with self._lock:
                if key in self._config:
                    return self._config[key]
            return default

        return getter

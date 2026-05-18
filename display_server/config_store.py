import threading


class ConfigStore:
    """Thread-safe store for the active mode id and its parameter values."""

    def __init__(self):
        self._lock = threading.RLock()
        self._mode_id = None
        self._config = {}
        self._version = 0

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
            self._version += 1

    @property
    def version(self):
        with self._lock:
            return self._version

    def update(self, values):
        with self._lock:
            values = dict(values)
            if "LINES" in values and isinstance(values["LINES"], list):
                values["LINES"] = "\n".join(str(line) for line in values["LINES"])
            self._config.update(values)
            self._version += 1

    def make_getter(self):
        """Return a get_config callable for display loops."""

        store = self

        def getter(key, default=None):
            with store._lock:
                if key in store._config:
                    return store._config[key]
            return default

        def config_version():
            return store.version

        getter.config_version = config_version
        return getter

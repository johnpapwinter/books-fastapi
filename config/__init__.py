import os
from functools import lru_cache
from .dev import DevSettings
from .prod import ProdSettings


@lru_cache
def get_settings():
    env = os.getenv("ENVIRONMENT", "dev")
    settings_map = {
        "dev": DevSettings,
        "prod": ProdSettings,
    }

    settings_class = settings_map.get(env, DevSettings)
    return settings_class()


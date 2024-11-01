from .base import Settings


class DevSettings(Settings):
    DEBUG: bool = True

    class Config:
        env_file = '.env.dev'



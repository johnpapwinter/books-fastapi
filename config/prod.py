from .base import Settings


class ProdSettings(Settings):
    DEBUG: bool = False

    class Config:
        env_file = '.env.prod'

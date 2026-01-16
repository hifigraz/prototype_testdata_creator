from ._config_class import Config


def get_config(file: str | None = None) -> Config:
    if file is not None:
        config = Config.load(filename=file)
    else:
        config = Config()
        config.DB_ENGINE = "sqlite"
        config.DB_HOST = ""
        config.DB_PORT = None
        config.DB_NAME = ":memory:"
        config.DB_USERNAME = ""
        config.DB_PASSWORD = ""
    return config

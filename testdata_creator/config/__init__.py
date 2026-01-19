# config module

from ._config_class import Config
from ._logging import get_logger
from ._testing_config import get_config as get_prod_config
from ._testing_config import get_config as get_test_config

__all__ = [
    "Config",
    "get_logger",
    "get_prod_config",
    "get_test_config",
]

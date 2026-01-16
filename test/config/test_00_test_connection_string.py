import testdata_creator.config


def test_00_test_configuration():
    IN_MEMORY_CONNECTION_STRING = "sqlite:///:memory:"
    config = testdata_creator.config.get_test_config()
    connection_string: str = config.connection_string
    assert IN_MEMORY_CONNECTION_STRING == connection_string

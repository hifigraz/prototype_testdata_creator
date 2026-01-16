import pydantic


class Config(pydantic.BaseModel):
    # Database configuration
    DB_ENGINE: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int | None = 5432
    DB_NAME: str = "testdata_creator"
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "postgres"

    @classmethod
    def load(cls, filename: str) -> Config:
        assert cls
        assert filename
        raise NotImplementedError()

    @property
    def connection_string(self) -> str:
        connection_string: str = f"{self.DB_ENGINE}://"
        if self.DB_USERNAME and self.DB_PASSWORD:
            connection_string = (
                f"{connection_string}{self.DB_USERNAME}:{self.DB_PASSWORD}"
            )
        connection_string = f"{connection_string}{self.DB_HOST}"
        if self.DB_PORT:
            connection_string = f"{connection_string}:${self.DB_PORT}"
        connection_string = f"{connection_string}/{self.DB_NAME}"
        return connection_string

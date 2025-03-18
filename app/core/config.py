from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore"
    )

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str

    flask_run_host: str
    flask_run_port: int

    def get_dbs(self):
        return (f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@"
                f"{self.postgres_host}/{self.postgres_db}")


settings = Settings()

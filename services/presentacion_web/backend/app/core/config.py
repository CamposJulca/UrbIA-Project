from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Variables esperadas desde .env
    thingsboard_url: str
    thingsboard_user: str
    thingsboard_password: str
    backend_port: int = 8000
    log_level: str = "INFO"

    # Configuración interna de Pydantic
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid"  # Para detectar cualquier variable inesperada
    )


settings = Settings()

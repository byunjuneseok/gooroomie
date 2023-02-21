from pydantic import BaseSettings


class Settings(BaseSettings):
    base_url: str
    frame_rate: int = 24
    health_check_interval: int = 60


settings = Settings()

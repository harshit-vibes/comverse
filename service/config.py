from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    lyzr_api_key: str = ""  # optional — can be provided per-request via X-Lyzr-Api-Key header
    comverse_agent_id: str = ""  # empty = create agent on first use


settings = Settings()

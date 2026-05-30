from utility.pydantic import PydanticBaseSettings


class WeatherConfig(PydanticBaseSettings):
    base_url: str
    api_key: str

    class Config:
        env_prefix = "WEATHER_"

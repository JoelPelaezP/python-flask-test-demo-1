from typing import Optional

from external_services.weather.client import BaseWeatherClient
from external_services.weather.config import WeatherConfig
from external_services.weather.mock_client import MockWeatherClient
from external_services.weather.weather_client import WeatherClient


def create_client(config: Optional[WeatherConfig] = None) -> BaseWeatherClient:
    if config is None:
        config = WeatherConfig()

    if config.base_url == "":
        return MockWeatherClient()
    else:
        return WeatherClient(config)

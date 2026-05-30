import requests

from external_services.weather.client import BaseWeatherClient
from external_services.weather.config import WeatherConfig


class WeatherClient(BaseWeatherClient):
    weather_config: WeatherConfig

    def __init__(self, weather_config: WeatherConfig):
        self.weather_config = weather_config

    def get_data(self):
        return self.__request("users")

    def __request(self, path: str):
        url = self.weather_config.base_url + path
        response: requests.Response = requests.get(
            url, headers={"x-api-key": self.weather_config.api_key}
        )
        return response.json()

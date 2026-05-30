from external_services.weather.client import BaseWeatherClient


class MockWeatherClient(BaseWeatherClient):
    def __init__(self):
        pass

    def get_data(self):
        return "mocked object"

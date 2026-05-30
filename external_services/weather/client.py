import abc


class BaseWeatherClient(abc.ABC):

    @abc.abstractmethod
    def get_data():
        pass

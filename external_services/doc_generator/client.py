import abc
from external_services.doc_generator.models import CreateSurveyRequest

class BaseDocumentGenratorClient(abc.ABC):
    @abc.abstractmethod
    def create_survey(request: CreateSurveyRequest):
        pass
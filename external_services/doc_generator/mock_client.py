from external_services.doc_generator.client import BaseDocumentGenratorClient
from external_services.doc_generator.models import CreateSurveyRequest


class MockDocumentGeneratorClient(BaseDocumentGenratorClient):
    def __init__(self):
        pass

    def create_survey(self, request: CreateSurveyRequest):
        return "Dummy.pdf"

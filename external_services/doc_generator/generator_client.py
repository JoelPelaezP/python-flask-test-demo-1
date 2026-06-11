import requests

from external_services.doc_generator.client import BaseDocumentGenratorClient
from external_services.doc_generator.config import DocumentgeneratorConfig
from external_services.doc_generator.models import CreateSurveyRequest


class DocumentGeneratorClient(BaseDocumentGenratorClient):
    config: DocumentgeneratorConfig

    def __init__(self, config: DocumentgeneratorConfig):
        self.config = config

    def create_survey(self, request: CreateSurveyRequest):
        return self.__request("document/create", request)

    def __request(self, path, request):
        url = self.config.base_url + path
        response: requests.Response = requests.post(url, json=request.dict())
        return response.json()

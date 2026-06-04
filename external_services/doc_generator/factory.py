from typing import Optional
from external_services.doc_generator.config import DocumentgeneratorConfig
from external_services.doc_generator.client import BaseDocumentGenratorClient
from external_services.doc_generator.mock_client import MockDocumentGeneratorClient
from external_services.doc_generator.generator_client import DocumentGeneratorClient

def create_client(config : Optional[DocumentgeneratorConfig] = None) -> BaseDocumentGenratorClient:
    if config is None:
        config = DocumentgeneratorConfig()

    if config.base_url == '':
        return MockDocumentGeneratorClient()
    else:
        return DocumentGeneratorClient(config)
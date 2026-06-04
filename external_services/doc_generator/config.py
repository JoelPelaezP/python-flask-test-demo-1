from utility.pydantic import PydanticBaseSettings

class DocumentgeneratorConfig(PydanticBaseSettings):
    base_url: str

    class Config():
        env_prefix = 'DOC_GENERATOR_'
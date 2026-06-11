from pydantic import BaseModel, ConfigDict


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    def __rich_repr__(self):
        for k, v in self.__repr_args__():
            yield k, v, None


class CreateSurveyRequest(CustomBaseModel):
    name: str
    lastName: str

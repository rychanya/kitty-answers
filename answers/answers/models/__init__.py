import abc
from bson import ObjectId


class CustomTypeValidateMixin(abc.ABC):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @abc.abstractclassmethod
    def validate(cls, v):
        ...


class OIDStr(ObjectId, CustomTypeValidateMixin):
    @classmethod
    def validate(cls, v: ObjectId):
        if isinstance(v, ObjectId):
            return v
        else:
            raise ValueError

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

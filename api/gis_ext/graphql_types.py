
from graphene import NonNull, Float, InputObjectType, ObjectType
__all__ = ["PointFieldType"]


class PointFieldType(ObjectType):
    """
    An extremely simple representation of a single coordinate
    """
    x = NonNull(Float)
    y = NonNull(Float)



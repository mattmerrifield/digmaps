
from graphene import NonNull, Float, InputObjectType
__all__ = ["PointFieldType"]


class PointFieldType(InputObjectType):
    """
    An extremely simple representation of a single coordinate
    """
    x = NonNull(Float)
    y = NonNull(Float)



import graphene

__all__ = ["PointFieldType"]


class PointFieldType(graphene.ObjectType):
    """
    An extremely simple representation of a single coordinate
    """

    x = graphene.Float()
    y = graphene.Float()



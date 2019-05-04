import graphene


class CoordinateType(graphene.ObjectType):
    """
    An extremely simple representation of a single coordinate
    """

    x = graphene.Float()
    y = graphene.Float()

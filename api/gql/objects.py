import graphene


class CoordinateType(graphene.ObjectType):
    x = graphene.Float()
    y = graphene.Float()

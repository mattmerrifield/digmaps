import graphene
from locations import objects as locations


class Query(locations.Query):
    """
    Leverage multiple inheritance to expose each module's query fields as top-level fields
    """
    pass


class Mutation(locations.Mutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

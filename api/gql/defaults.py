from graphene_django_extras import LimitOffsetGraphqlPagination


class DefaultPaginator(LimitOffsetGraphqlPagination):
    def __init__(self, *args, **kwargs):
        if not kwargs.get("ordering"):
            kwargs["ordering"] = "id"
        super(DefaultPaginator, self).__init__(*args, **kwargs)

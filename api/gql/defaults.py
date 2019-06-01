from graphene_django_extras import LimitOffsetGraphqlPagination


# Set up a default pagination class
class DefaultPaginator(LimitOffsetGraphqlPagination):
    def __init__(self, *args, **kwargs):
        # Default ordering is by 'id'
        kwargs["ordering"] = kwargs.get("ordering", "id")

        # If we don't ask for pagination... we get the whole queryset
        # This *is* a bit of a footgun, so you need to write
        # responsible frontend code when you expect to get
        # huge piles of results.
        #
        # However, the tradeoff is that if you *don't* write
        # responsible code, it'll fail noisily (by making
        # the page unbearably slow, instead of just
        # hiding any results after the first 20.
        #
        # The other option here would have been (IMO) to
        # have a paginating container with a `next: ...`
        # and `results: [...]` kind of structure.
        kwargs["max_limit"] = None
        kwargs["default_limit"] = None
        super(DefaultPaginator, self).__init__(*args, **kwargs)

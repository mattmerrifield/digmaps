from rest_framework import serializers
from bibliography import models


class AuthorSummarySerializer(serializers.ModelSerializer):
    """
    Simple, flat author representation, suitable for either nesting or a flat object for listing.
    """
    class Meta:
        model = models.Author
        fields = (
            'id',
            'first_name',
            'last_name',
        )


class PublicationSummarySerializer(serializers.ModelSerializer):
    """
    Simple, flat publication summary, suitable for nesting or simple object listing.
    """
    authors = AuthorSummarySerializer(many=True)

    class Meta:
        model = models.Publication
        depth = 2
        fields = (
            'id',
            'title',
            'citation_text',
        )


class AuthorSerializer(AuthorSummarySerializer):
    """
    More complex representation, with all nested publications summaries.
    """
    publications = PublicationSummarySerializer()

    class Meta(AuthorSummarySerializer.Meta):
        depth = 2
        fields = AuthorSummarySerializer.Meta.fields + ('publications')


class PublicationSerializer(PublicationSummarySerializer):
    """
    More complete representation, with nested Author summaries.
    """
    authors = AuthorSummarySerializer(many=True)

    class Meta(PublicationSummarySerializer.Meta):
        depth = 2
        fields = PublicationSummarySerializer.Meta.fields + ('authors')

from django.db import models


class Author(models.Model):
    """
    Somebody who gets credit for writing something interesting
    """
    first_name = models.CharField(max_length=100, default='', blank=True)
    last_name = models.CharField(max_length=100, default='', blank=True)


class Publication(models.Model):
    """
    A particular published bit of information. One of:

     - Journal Article
     - Survey data from website
     - Book
     - Conference Talk

    etc.
    """
    title = models.CharField(max_length=100)
    citation_text = models.TextField(default='', help_text="Appropriately formatted citation string for this publication")
    authors = models.ManyToManyField(Author)

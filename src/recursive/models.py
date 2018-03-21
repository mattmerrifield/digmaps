from django.db import models


class RecursiveModelQuerySet(models.QuerySet):
    """
    Provides convenience methods for querying with .parent and .children
    across multiple levels
    """
    def parents_of(self, obj):
        """
        Returns all parents, grandparents, great-grandparents, etc.
        """
        parents = obj.parents(include_self=False)
        return self.filter(pk__in=[p.pk for p in parents])

    def children_of(self, obj):
        """
        Returns all objects which have the given one somewhere below them in
        """
        children = obj.children
        return self.filter(pk__in=[c.pk for c in children])


class RecursiveModel(models.Model):
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name='children'
    )

    objects = RecursiveModelQuerySet.as_manager()

    class Meta:
        abstract = True

    def ancestors(self, include_self=True, depth=None):
        """
        Returns a list like:

          [parent, grandparent, great-grandparent, ..., (great)^n-grandparent]

        describing the 'ancestors' of this recursively-associated model.
        """
        ancestors = [self] if include_self else []
        parent = self.parent
        while parent is not None:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors

    def descendants(self, include_self=True, depth=None):
        """
        Returns a list of all children, all grandchildren, all
        great-grandchildren, etc.
        """
        family = []
        depth = depth - 1 if depth is not None else None
        if include_self:
            family.append(self)
        for r in self.children.all():
            family.extend(r.descendants(include_self=True, depth=depth))
            if depth <= 0:
                return family
        return family
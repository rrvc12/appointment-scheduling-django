from django.http import Http404
from django.shortcuts import get_object_or_404
from typing import Dict, Any
from django.db.models import ManyToManyField


def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


def update_object(instance, fields: Dict[str, Any]):
    """
    Update the fields of an object and save it to the database.
    Only the fields that are present in the dictionary will be updated.
    """

    for field in fields:
        if hasattr(instance, field):
            model_field = instance._meta.get_field(field)
            value = fields[field]
            if isinstance(model_field, ManyToManyField):
                # Handle ManyToMany fields separately
                related_manager = getattr(instance, field)
                related_manager.set(value)
            else:
                setattr(instance, field, value)

        else:
            raise ValueError(
                f"Field {field} does not exist on {instance.__class__.__name__}"
            )

    instance.full_clean()
    instance.save()

    return instance


def delete_object(instance):
    """
    Delete the object from the database.
    """
    instance.delete()

from django import template
from django.urls import reverse

register = template.Library()


def action_links(object):
    model_name = object._meta.model_name
    actions = {
        "detail": {
            "url": reverse(f"{model_name}-detail", kwargs={"pk": object.pk}),
            "text": "View",
        },
        "update": {
            "url": reverse(f"{model_name}-update", kwargs={"pk": object.pk}),
            "text": "Edit",
        },
        "delete": {
            "url": reverse(f"{model_name}-delete", kwargs={"pk": object.pk}),
            "text": "Delete",
        },
    }
    return actions


@register.inclusion_tag("neapolitan/partial/detail.html")
def object_detail(object, fields):
    """
    Renders a detail view of an object with the given fields.

    Inclusion tag usage::

        {% object_detail object fields %}

    Template: ``neapolitan/partial/detail.html`` - Will render a table of the
    object's fields.
    """

    def iter():
        for f in fields:
            mf = object._meta.get_field(f)
            yield (mf.verbose_name, mf.value_to_string(object))

    return {"object": iter()}


@register.inclusion_tag("neapolitan/partial/list.html")
def object_list(objects, fields):
    """
    Renders a list of objects with the given fields.

    Inclusion tag usage::

        {% object_list objects fields %}

    Template: ``neapolitan/partial/list.html`` — Will render a table of objects
    with links to view, edit, and delete views.
    """

    headers = [objects[0]._meta.get_field(f).verbose_name for f in fields]
    object_list = [
        {
            "object": {f: getattr(object, f) for f in fields},
            "fields": [
                {"name": f, "value": object._meta.get_field(f).value_to_string(object)} for f in fields
            ],
            "actions": action_links(object),
        }
        for object in objects
    ]

    return {
        "headers": headers,
        "object_list": object_list,
    }

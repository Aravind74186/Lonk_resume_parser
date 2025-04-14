import json
from django import template

register = template.Library()

@register.filter
def tojson(value):
    """
    Converts a Python object into a JSON string.
    """
    return json.dumps(value)

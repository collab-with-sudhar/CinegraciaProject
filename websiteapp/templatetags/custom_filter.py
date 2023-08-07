from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def replace_slashes_with_spaces(value):
    return value.replace('/', ' ')

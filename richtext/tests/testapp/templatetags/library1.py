from django import template

register = template.Library()

@register.filter
def my_higher(value):
    return value.upper()
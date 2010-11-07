from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def my_bolder(value):
    return "<b>" + value + "</b>"
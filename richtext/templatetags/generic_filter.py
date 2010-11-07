from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from django.template import Parser
from django.template.defaulttags import load

p = Parser([])
def load_library(lib_name):
    load(p, type("", (), {"contents": "load %s" % lib_name}))    

register = template.Library()

if hasattr(settings, "PRETTIFY_FILTERS"):
    libraries = set()
    filters = []
    for f in settings.PRETTIFY_FILTERS:
        lib_name, func_name = f.split(".")
        libraries.add(lib_name)
        filters.append(func_name)
        
    for lib_name in libraries:
        load_library(lib_name)

@register.filter
def prettify(val):
    for f in filters:
        val = p.filters[f](val)
    return mark_safe(val)
    
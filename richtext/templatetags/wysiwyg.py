#Inspired (and greatly simplified) from http://github.com/pydanny/django-wysiwyg/tree/master/django_wysiwyg

from django import template
from django.template.loader import render_to_string
from django.template.context import RequestContext

register = template.Library()

 
@register.simple_tag
def wysiwyg_setup(editor_name, request=None):
    ctx = RequestContext(request) if request else None
    return render_to_string(
        "wysiwyg/%s/setup.html" % editor_name,
        context_instance=ctx
    )
 
 
@register.simple_tag
def wysiwyg_instantiate(editor_name, field_id, request=None):
    ctx = RequestContext(request) if request else None
    return render_to_string(
        "wysiwyg/%s/instantiate.html" % editor_name,
        { 'field_id': field_id },
        context_instance=ctx
    )

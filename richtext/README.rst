WYSIWYG
=======

First, you need to copy the js/css provided by your favourite WYSIWYG widget in your media folder, wherever you like (e.g. /media/js/markitup/).

In the admin
------------

Override the 'change_form.html' template in for your app's admin. E.g. in /templates/admin/blog/entry/change_form.html
and add something like the following:

{% extends "admin/change_form.html" %}
{% load wysiwyg %}

{% block extrahead %}
    {{ block.super }}
    
    {% wysiwyg_setup "markitup-markdown" %}
    {% wysiwyg_instantiate "markitup-markdown" "id_excerpt" %}
    {% wysiwyg_instantiate "markitup-markdown" "id_body" %}
{% endblock %}

Note: the above can be used in any template, not just in the admin's.

Richtext ships with sensible defaults (e.g. for markitup or tinymce). To override those or to use other widgets, simply add templates in /template/richtext/<widget-name>/setup.html and instantiate.html

Generic filter usage
====================

'prettify' is a generic template filter which applies a list of filters,
which were found in the template variable 'PRETTIFY_FILTERS'

The usage is::

    {% load generic_filter %}
    {{ dat | prettify }}
    
The syntax for the template variable is a tuple of strings, each string
is <template_library>.<filter_name>




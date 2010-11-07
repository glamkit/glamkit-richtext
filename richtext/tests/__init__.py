import unittest

from django.template import Template, Context
from django.core.management import call_command
from django.db.models.loading import load_app
from django import template
from django.template.loaders import app_directories

from django.conf import settings

class RichTextTest(unittest.TestCase):
    def render(self, dat):
        return self.template.render(Context({"dat": dat}))
            
    def setUp(self):        
        settings.PRETTIFY_FILTERS = ("library1.my_higher", "library2.my_bolder")
        self.old_INSTALLED_APPS = settings.INSTALLED_APPS
        settings.INSTALLED_APPS += ['richtext.tests.testapp']
        load_app('richtext.tests.testapp')
        
        # since django's r11862 templatags_modules and app_template_dirs are cached
        # the cache is not emptied between tests
        # clear out the cache of modules to load templatetags from so it gets refreshed
        template.templatetags_modules = []
        
        # clear out the cache of app_directories to load templates from so it gets refreshed
        app_directories.app_template_dirs = []
        # reload the module to refresh the cache
        reload(app_directories)
        # reload generic_filter to recreate the filters
        from ..templatetags import generic_filter
        reload(generic_filter)
        self.template = Template("{% load generic_filter %}{{ dat|prettify }}")

    def tearDown(self):
        settings.INSTALLED_APPS = self.old_INSTALLED_APPS

    def testBasic(self):
        self.assertEquals(self.render("howdy"), u"<b>HOWDY</b>")

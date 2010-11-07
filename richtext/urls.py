from django.conf.urls.defaults import *


urlpatterns = patterns('richtext.views',
    (r'^format_preview/$', 'format_preview'),
)

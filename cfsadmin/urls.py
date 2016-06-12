"""
Defines the URL mappings of project.
"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^api/$', 'cfsadmin.views.api_root'),
    url(r'^api/', include('cfsadmin.apps.api.urls')),
)

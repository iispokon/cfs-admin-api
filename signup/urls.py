"""
Defines the URL mappings of project.
"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^api/$', 'signup.views.api_root'),
    url(r'^api/', include('signup.apps.api.urls')),
)

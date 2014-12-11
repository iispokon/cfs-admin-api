"""
Defines the URL mappings of API module.
"""
from django.conf.urls import patterns, url
from signup.apps.api.views import User, Authenticate

urlpatterns = patterns(
    '',
    url(r'^user/$', User.as_view(), name='user'),
    url(r'^authenticate/$', Authenticate.as_view(), name='auth'),
)

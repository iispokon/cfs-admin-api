"""
Defines the URL mappings of API module.
"""
from django.conf.urls import patterns, url
from cfsadmin.apps.api.views import User, Authenticate, AccountState, Delete, FolderCreate, FolderDelete

urlpatterns = patterns(
    '',
    url(r'^user/$', User.as_view(), name='user'),
    url(r'^user/delete/$', Delete.as_view(), name='delete'),
    url(r'^authenticate/$', Authenticate.as_view(), name='auth'),
    url(r'^accountState/$', AccountState.as_view(), name='AS'),
    url(r'^folder/create/$', FolderCreate.as_view(), name='folder_create'),
    url(r'^folder/delete/$', FolderDelete.as_view(), name='folder_delete')
)

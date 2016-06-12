"""
Defines the views for project.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    """
    Root view of the api.
    """
    return Response({
        'user': reverse('user', request=request, format=format)
    })

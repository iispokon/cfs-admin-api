from cloudfs.session import Session
from cloudfs.private.rest_api_adapter import CloudFSRESTAdapter


class UserSession(Session):

    def __init__(self, endpoint, client_id, client_secret, auth_key):
        super(UserSession, self).__init__(endpoint, client_id, client_secret)
        self.rest_interface = CloudFSRESTAdapter(endpoint, client_id,
                                                 client_secret, auth_key)
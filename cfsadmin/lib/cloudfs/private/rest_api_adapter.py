import requests
import datetime
import base64
import hmac
import json
import hashlib
import threading
from urlparse import urlparse
from copy import deepcopy
from utils import request_to_string, response_to_string, utf8_quote_plus, make_utf8
from ..errors import error_from_response, session_not_linked_error, missing_argument, invalid_argument, SessionNotLinked
from cloudfs_paths import rest_endpoints, ExistValues, VersionConflictValue, RestoreValue

# more detailed debugging info, including redirects, but without any filtering. RIP terminal.
debug = False

if debug:
    import logging
    import httplib as http_client

    http_client.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


class CloudFSRESTAdapter(object):
    def __init__(self, url_root, client_id, secret, auth_token=''):
        self.bc_conn = CloudFSConnection(url_root, client_id, secret, auth_token)
        self.linked = False
        self.debug_count = 0

    def wait_for_downloads(self, timeout=None):
        """Wait for any threaded downloads that have not completed

        :param timeout: Float number of seconds to wait or None to wait until downloads are done. Defaults to None.
        :return: True if all downloads are done, False otherwise.
        """
        return self.bc_conn.join_threads(timeout)

    def get_copy(self):
        """Returns a copy of the rest interface

        get_copy exists to centralize invalidation of a session.
        Current behavior is to allow 'children' of the session to continue
        refreshing their information as time goes on. However, we can change
        behavior in the future.

        :returns:   A CloudFSRESTAdapter that is authenticated to the same account as self.

        """
        return deepcopy(self)

    def debug_requests(self, count):
        """Print information for future requests.
        Warning: These print statements do not censor personal information or authentication data.
        Do not transmit in the clear under any circumstances!

        :param count:       Number of requests to print

        :returns:           None

        """
        self.debug_count += count

    def get_last_request_log(self):
        """Get string of last request. Useful for logging requests.
        Warning: These string do not censor personal information or authentication data.
        Do not transmit in the clear under any circumstances!

        Will return an empty string when no request has been made.
        :return: String of last request and response.
        """

        return self.bc_conn.last_request_log

    def is_linked(self):
        """Return if this CloudFSRESTAdapter can currently make requests.
        Does not use up an API request.

        :returns:       True if this is authenticated to the server. False otherwise.

        """
        try:
            self.ping()
            self.linked = True
        except SessionNotLinked:
            self.linked = False

        return self.linked

    def unlink(self):
        """Clear current authentication information associated with this CloudFSRESTAdapter

        :returns:       None

        """
        self.bc_conn.auth_token = ''
        self.linked = False

    def get_latest_header_info(self):
        """Return the latest version if the information encoded in response headers.
        Currently, this is some storage quota information (number of bytes stored, current limit).
        It's reflected in the Account object of the SDK.

        :returns:   Dictionary with information encoded in the headers.

        """
        return self.bc_conn.header_information

    def _make_request(self, request_name, path=None, data={}, params={}, headers={},  # standard arguments
                      response_processor=None, files=None, oauth_request=False, background=False, share_key=None,
                      version=None, current_date=None):  # special case arguments
        """Makes a request after merging standard request parameters with user-supplied data

        :param request_name:        Index into the rest_endpoints table in cloudfs_paths.py.
        :param path:                Path in the CloudFS Filesystem. Optional.
        :param data:                Post data in encoded in dictionary. Optional.
        :param params:              URL Parameters in dictionary. Optional.
        :params headers:            Headers in dictionary. Optional.
        :param response_processor:  Function to process response value. Optional.
        :param files:               Files to post. Optional.
        :param oauth_request:       Flag to indicate if this is an 'oauth' request (does not follow strict oauth flow, see CloudFS docs). Optional.
        :param background:          Flag to indicate if this request should return before completing the entire body

        :returns:   Dictionary of JSON request or string of response body. True or False for oauth_request.
        :raises ValueError:             request_name is not found in rest_endpoints.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS returns an error.

        """
        try:
            request_data = rest_endpoints[request_name]
        except ValueError:
            raise ValueError('Could not find friendly rest endpoint named "{}".'.format(request_name))

        # need to re-create to avoid modifying rest_endpoints or default values
        merged_data = {}
        merged_params = {}

        merged_data.update(request_data['data'])
        merged_data.update(data)
        merged_params.update(request_data['params'])
        merged_params.update(params)

        url = request_data['url']
        if url.find('{share_key}') > 0:
            if not share_key:
                raise missing_argument('share_key')
        url = url.format(path=str(path), share_key=str(share_key), version=str(version))

        # track this here
        if self.debug_count > 0:
            self.bc_conn.debug_next_request()
            self.debug_count -= 1

        if oauth_request:
            return self.bc_conn.oauth_request(url, merged_data, merged_params, request_data['method'],
                                              current_date=current_date)
        else:
            return self.bc_conn.request(url, merged_data, merged_params, files, request_data['method'],
                                        response_processor, headers, background)

    def create_account(self, username, password, email=None, first_name=None, last_name=None, account_plan_uuid=None,
                       current_date=None, tkey=False):
        """Create a user account associated with your CloudFS account.

        Warning: This method is currently broken, and will almost certainly 500. If you're interested, or the method has
        since been fixed server side, call the method with force=true. The request format is not expected to change.


        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Create%20Account.html

        :param username:    Username for the user, must be at least 4 characters and less than 256 characters.
        :param password:    Password for the user, must be at least 6 characters and has no length limit.
        :param email:       Email address for user. Optional.
        :param first_name:  Users' first name. Optional
        :param last_name:   Users' last name. Optional
        :param debug:       If true, will print the the request and response to stdout.
        :param force:       Method is currently not supported, and will throw an exception unless force is specified.
        :return:            Dictionary containing JSON of new users' profile.
        """
        data = {
            'username': username,
            'password': password
        }
        if email:
            data['email'] = email
        if first_name:
            data['first_name'] = first_name
        if last_name:
            data['last_name'] = last_name

        request_string = 'create account'

        if tkey:
            request_string = 'create tkey account'
            if account_plan_uuid:
                print "account plan = {}".format(account_plan_uuid)
                data['account_plan_uuid'] = account_plan_uuid

        response = self._make_request(request_string, data=data, oauth_request=True, current_date=current_date)
        print "response1:{}".format(response)
        return response['result']

    def delete_account(self, user_id):

        data = {
            'username': user_id
        }
        response = self._make_request('delete account', data=data, oauth_request=True)
        print "response1:{}".format(response)

        if response['error'] is not None:
            return response['error']

        return response['result']

    def account_state(self, user_id, username=None, first_name=None, last_name=None, plan_code=None,
                      expiration_date=None, grace=None, ignore_otl=None, plan_transition=None):
        data = {
            'user_id': user_id
        }
        if username:
            data['username'] = username
        if first_name:
            data['first_name'] = first_name
        if last_name:
            data['last_name'] = last_name
        if plan_code:
            data['plan_code'] = plan_code
        if expiration_date:
            data['expiration_date'] = expiration_date
            print "expiration date = {}, plan code={}".format(expiration_date, plan_code)
        if grace:
            data['grace'] = grace
        if ignore_otl:
            data['ignore_otl'] = ignore_otl
        else:
            data['ignore_otl'] = 'false'
        if plan_transition:
            data['plan_transition'] = plan_transition

        response = self._make_request('account state', data=data, oauth_request=True)
        print "response1:{}".format(response)

        if response['error'] is not None:
            return response['error']

        return response['result']

    def authenticate(self, username, password):
        """Authenticate to CloudFS using the provided user details.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Oauth2%20Password%20Credentials%20Grant.html

        :param username:        Username of the user.
        :param password:        Password of the user.

        :returns: True if successful and False otherwise.

        """
        data = {
            'username': username,
            'password': password
        }
        result = self._make_request('get oauth token', data=data, oauth_request=True)
        print "/token result={}".format(result)
        if 'access_token' in result:
            return True

        return False

    def ping(self):
        """Check that authentication is still valid

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Ping.html

        :returns:   Empty string if successful, exception if not.
        :raises:    SessionNotLinked if the CloudFSRESTAdapter is not authenticated.

        """
        return self._make_request('ping')

    def list_folder(self, path):
        """List the contents of the folder.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/List%20Folder.html

        :param path:    Path to folder to list.

        :returns:   Dictionary representation of JSON response.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        return self._make_request('list folder', path)

    def user_profile(self):
        """Returns the profile of the currently authenticated user.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Get%20Profile.html

        :returns:   Dictionary encoding of the user profile information.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        return self._make_request('get user profile')

    def change_user_profile(self, data):
        """Update the user profile.
        Currently mostly non-functional.

        :param data:    Dictionary of settings to change

        :returns:   Dictionary with a key indicating success.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        return self._make_request('change user profile', data=data)

    def create_folder(self, path, name, exists=ExistValues.overwrite):
        """Create a folder.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Create%20Folder.html

        :param path:    Parent folder for the new folder.
        :param name:    Name of the new folder.
        :parm exists:   Behavior if folder name already exists. Default Value overwrite

        :returns:   Dictionary encoded information about the new folder.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        print "this is the create_folder method...path={} name={}, exists={}".format(path, name, exists)

        data = {
            'name': name,
            'exists': exists
        }
        return self._make_request('create folder', path, data=data)

    def delete_folder(self, path, commit=False, force=False):
        """Delete a folder.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Delete%20Folder.html

        :param path:        Path to folder that will be deleted.
        :param commit:      If true, will permanently remove the folder. Will move to trash otherwise. Defaults to False.
        :param force:       If true, will delete folder even if it contains Items. Defaults to False.

        :returns:   Dictionary with keys for success and the deleted folders last version.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        params = {
            'commit': str(commit),
            'force': str(force),
        }

        return self._make_request('delete folder', path, params=params)

    def delete_file(self, path, commit=False):
        """Delete a file.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Delete%20File.html

        :param path:        Path to file to delete.
        :param commit:      If true, will permanently remove the file. Will move to trash otherwise. Defaults to False.

        :returns:   Dictionary with keys for success and the deleted files last version.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        params = {
            'commit': str(commit),
        }

        return self._make_request('delete file', path, params=params)

    def _common_file_operation(self, verb, path, destination, destination_name, exists=None):
        data = {
            'to': destination,
            'name': destination_name
        }
        if exists:
            if ExistValues.legal_value(exists):
                data['exists'] = exists
            else:
                ExistValues.raise_exception(exists)

        return self._make_request(verb, path, data=data)

    def move_file(self, path, destination, destination_name, exists=None):
        """Move a file to another location.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Move%20File.html

        :param path:                Location of the item to move.
        :param destination:         Path to destination folder.
        :param destination_name:    Name of new item to create in the destination folder.
        :param exists:              How to handle if an item of the same name exists in the destination folder. Defaults to rename.

        :returns:   Details of the new item in a dictionary.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        return self._common_file_operation('move file', path, destination, destination_name, exists)

    def move_folder(self, path, destination, destination_name, exists=None):
        """Move folder to another location.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Move%20Folder.html

        :param path:                Location of the item to move.
        :param destination:         Path to destination folder.
        :param destination_name:    Name of new item to create in the destination folder.
        :param exists:              How to handle if an item of the same name exists in the destination folder. Defaults to rename.

        :returns:   Details of the new item in a dictionary.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        return self._common_file_operation('move folder', path, destination, destination_name, exists)

    def copy_file(self, path, destination, destination_name, exists=None):
        """Create a copy of this file at another location.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Copy%20File.html

        :param path:                Location of the item to move.
        :param destination:         Path to destination folder.
        :param destination_name:    Name of new item to create in the destination folder.
        :param exists:              How to handle if an item of the same name exists in the destination folder. Defaults to rename.

        :returns:   Details of the new item in a dictionary.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        return self._common_file_operation('copy file', path, destination, destination_name, exists)

    def copy_folder(self, path, destination, destination_name, exists=None):
        """Create a copy of this folder at another location.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Copy%20Folder.html

        :param path:                Location of the item to move.
        :param destination:         Path to destination folder.
        :param destination_name:    Name of new item to create in the destination folder.
        :param exists:              How to handle if an item of the same name exists in the destination folder. Defaults to rename.

        :returns:   Details of the new item in a dictionary.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        return self._common_file_operation('copy folder', path, destination, destination_name, exists)

    def _alter_meta(self, verb, path, data, whitelist, conflict):
        def remove(x):
            if x not in whitelist:
                del data[x]

        map(remove, data.keys())
        if conflict:
            if not VersionConflictValue.legal_value(conflict):
                VersionConflictValue.raise_exception(conflict)
            data['version-conflict'] = conflict
        if 'version' not in data:
            raise missing_argument('data.version')

        return self._make_request(verb, path, data=data)

    def file_alter_meta(self, path, data, conflict=None):
        """Alter the meta data of a file.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Alter%20File%20Meta.html

        :param path:        Path of file to alter.
        :param data:        Dictionary of value keys and their new values.
        :param conflict:    Behavior if the file has been updated since retrieving it from Cloudfs.

        :returns:   Dictionary with new file details stored under the 'meta' key.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        whitelist = ['name', 'date_created', 'date_meta_last_modified', 'application_data', 'mime', 'version']
        return self._alter_meta('alter file meta', path, data, whitelist, conflict)

    def folder_alter_meta(self, path, data, conflict=None):
        """Alter the meta data of a folder.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Alter%20Folder%20Meta.html

        :param path:        Path of folder to alter.
        :param data:        Dictionary of value keys and their new values.
        :param conflict:    Behavior if the folder has been updated since retrieving it from Cloudfs.

        :returns:   Dictionary with new folder details stored under the 'meta' key.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        whitelist = ['name', 'date_created', 'date_meta_last_modified', 'application_data', 'version']
        return self._alter_meta('alter folder meta', path, data, whitelist, conflict)

    def file_get_meta(self, path):
        """Get the meta data for a single file.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Get%20File%20Meta.html

        :param path:    Path to file.

        :returns:   Dictionary with file details.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        return self._make_request('get file meta', path)

    def folder_get_meta(self, path):
        """Get the meta data for a single folder.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Get%20Folder%20Meta.html

        :param path:    Path to file.

        :returns:   Dictionary with folder details.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        return self._make_request('get folder meta', path)

    def upload(self, path, file, exists=None, reuse_fallback=None, reuse_attributes=None):
        """Upload a file to Cloudfs.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Upload%20File.html

        :param path:                Folder to upload this file to.
        :param file:                File information. Formatted like POSTing files in Requests.
        :param exists:              Determines behavior if a file of the same name exists. Default behavior is fail.
        :param reuse_fallback:      Not implemented.
        :param reuse_attributes:    Not implemented.

        :returns:                       Dictionary of new file details.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.

        """
        data = {}
        if exists:
            data['exists'] = exists
        if reuse_fallback or reuse_attributes:
            if not reuse_fallback:
                raise missing_argument('reuse-fallback')
            if not reuse_attributes:
                raise missing_argument('reuse-attributes')
                # data['reuse-fallback'] = reuse_fallback
                # data['reuse-attributes'] = reuse_attributes
        return self._make_request('upload file', path, data=data, files=file)

    def download(self, path, save_data_function, range=None, background=False):
        """Download a file.
        If background is set to true, the rest adapter will do its best to allow the download to finish. This means that __del__ will block more-or-less forever.
        See the finish_downloads method on session to deal with this.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Download%20File.html

        :param path:                Path to file to download.
        :param save_data_function:  Function will be called with the response as an argument in order to process the requests' content. Used to save file in the background.
        :param range:               List or tuple with two values containing the range of the request. Second value may be an empty string, but must exist and not be none. Defaults to entire file.
        :param background:          If true, request will return immediately and save_data_function will run in a thread. Defaults to False.

        :returns:                       Empty string.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        :raises InvalidArgument:        Based on CloudFS Error Code.

        """
        headers = {}
        if range:
            if not hasattr(range, '__iter__') or len(range) != 2:
                raise invalid_argument('range argument', 'list type of length 2', range)
            headers['Range'] = 'bytes={}-{}'.format(range[0], range[1])
        return self._make_request('download file', path, response_processor=save_data_function, headers=headers,
                                  background=background)

    def list_trash(self, path):
        """List the contents of a folder in trash.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Browse%20Trash.html

        :param path:        Path to folder to list.

        :returns:                       Dictionary representation of items in folder.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        return self._make_request('list trash', path)

    def delete_trash_item(self, path):
        """Permanently remove an item from the users' filesystem.

        Warning: After calling this interface, there is _no way_ to retrieve the item deleted.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Delete%20Trash%20Item.html

        :param path:        Path to item to delete.
        :return:            None
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        return self._make_request('delete trash item', path)

    def restore_trash_item(self, path, restore_method=RestoreValue.fail, method_argument=None):
        """Move an item from trash to the mail filesystem.

        Behavior for this call depends on the method selected.
        fail: Will attempt to move the item to its previous location.
        rescue: Will attempt to move the item to a different location, supplied in method_argument.
        recreate: Will attempt to create a new folder at the filesystem root with the name

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Recover%20Trash%20Item.html

        :param path:            Path to item to delete.
        :param restore_method:  Determines method used to restore item.
        :param method_argument: Expected contents determined by value of restore_method
        :return:
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        if not RestoreValue.legal_value(restore_method):
            raise RestoreValue.raise_exception(restore_method)
        data = {'restore': restore_method}
        if restore_method == RestoreValue.rescue:
            if hasattr(method_argument, 'path'):
                method_argument = method_argument.path()
            data['rescue-path'] = method_argument
        elif restore_method == RestoreValue.recreate:
            data['recreate-path'] = method_argument

        return self._make_request('recover trash item', path, data=data)

    def create_share(self, paths):
        """Create a share from one or more paths

        The resulting share directory structure is predictable, but not obvious.

        If the share consists of a single folder, the 'contents' of the share will be the
        contents of that folder. Receiving the share will add the single folder to the users' drive.

        If the share consists of multiple items (or a single non-folder item), the 'contents' of the
        share will be those items (as if a new folder were created to hold them). Receiving that
        share will add all those items to the path the share is receieved on.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Create%20Share.html

        :param paths:   List of items in the filesystem that will be in the base directory
        :return:        Dictionary of information about share, including the share key.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """

        # requests doesn't officially support multiple post parameters with the same name.
        # however, you can work around this by passing in a container with __iter__.
        # If there's only one item, it should not be in a container, as requests will just str() it.

        if hasattr(paths, '__iter__') and len(paths) == 1:
            paths = paths[0]

        data = {
            'path': paths
        }

        return self._make_request('create share', data=data)

    def browse_share(self, share, path=None):
        """List the contents of a share

        Returns a list of items. Most functions (downloading, moving, making changes) are disabled due to the items
        being in the share. To download them or make changes, they must be recieved onto a user filesystem.

        If the share is locked, this call will throw an exception.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Browse%20Share.html

        :param share:   Key for the share.
        :param path:    Internal path for the share. Optional, defaults to root.
        :return:        A dictionary representation of the JSON describing the items in the share.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        if not path:
            path = '/'

        return self._make_request('browse share', path, share_key=share)

    def delete_share(self, share):
        """Deletes the specified share.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Delete%20Share.html

        :param share:   Key for the share.
        :return:        A dictionary representation of JSON indicating the result.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """

        return self._make_request('delete share', share_key=share)

    def list_shares(self):
        """List the shares created by the current user.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/List%20Shares.html

        :return:                        A dictionary representation of the JSON describing the shares.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """

        return self._make_request('list shares')

    def receive_share(self, share, receive_path=None, exists=ExistValues.rename):
        """Add contents of the share to the current users' filesystem.

        Behaves differently depending on how the share was crated.
        See create_share for notes on behavior of this command.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Receive%20Share.html

        :param share:           Key for the share.
        :param receive_path:    Path in users' filesystem to add the contents of the share to. Optional, defaults to root.
        :param exists:          How to handle if an item of the same name exists in the destination folder. Defaults to rename.
        :return:                Dictionary of JSON representation of items created by receiving this share on the users' filesystem. (phew)
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        data = {
            'exists': exists
        }
        if receive_path:
            data['path'] = str(receive_path)

        return self._make_request('receive share', data=data, share_key=share)

    def unlock_share(self, share, password):
        """Unlock the share with its password so the current user can access its contents.

        :param share:       Key for the share.
        :param password:    Password for the share.
        :return:            None
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        data = {
            'password': password
        }
        return self._make_request('unlock share', data=data, share_key=share)

    def alter_share_info(self, share, password=None, new_password=None, new_name=None):
        """Change properties of the specified share.

        This is not intended to be used to change the contents of the share.

        :param share:           Key for the share.
        :param password:        Password for share if password is set. Optional, default is None.
        :param new_password:    Used to set a new password for the share. If the password is currently set, it must be supplied in the password argument.
        :param new_name:        New name for the share.
        :return:                Dictionary of the JSON representation of the share.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        data = {}
        if password:
            data['current_password'] = password
        if new_password:
            data['password'] = new_password
        if new_name:
            data['name'] = new_name

        return self._make_request('alter share info', data=data, share_key=share)

    def list_file_versions(self, path, start=0, stop=None, limit=10):
        """List the versions of a file

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/List%20File%20Versions.html

        :param path:    Path to current location of file in the filesystem.
        :param start:   Lowest version number to list. Optional, defaults to listing all file versions.
        :param stop:    Last version of the file to list. Optional, defaults to listing the most recent version of the file.
        :param limit:   Limit on number of versions returned. Optional, defaults to 10.
        :return:        Dictionary representation of JSON describing previous versions of the file.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        params = {
            'start-version': start,
            'limit': limit
        }
        if stop:
            params['stop-version'] = stop
        return self._make_request('list file versions', path, params=params)

    def list_single_file_version(self, path, version):
        """List a single version of a file.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/List%20Single%20File%20Version.html

        :param path:    Path to current location of file in the filesystem.
        :param version: Version of file to get.
        :return:        Dictionary representation of JSON describing previous version of the file.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        return self._make_request('list single file version', path, version=version)

    def promote_file_version(self, path, version):
        """Create a new version of a file using the metadata and contents of a previous version.

        The current file will be replaced with a previous version of that file. File will be identical to prevous
        version, except for file history. Current version will be added to history with current number and the new
        version will get a new version number.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/Promote%20File%20Version.html

        :param path:        Path to current location of file in the filesystem.
        :param version:     Number of version to promote
        :return:            Dictionary of JSON describing the promoted version of the file.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        return self._make_request('promote file version', path, version=version)

    def action_history(self, start=-10, stop=None):
        """List previous actions taken by the current user.

        The list of actions is in a series of JSON dictionaries which include the version number associated
        and other information that will vary with the action described. List begins at version 0 and counts up.

        Action history was designed based on the internal needs of Bitcasa, but should be useful for any developer.
        If your CloudFS application makes more than a cursory use of the action history, we encourage you to get in
        contact with us.

        REST Documentation: https://www.bitcasa.com/cloudfs-api-docs/api/List%20History.html

        :param start:       First version number to list. If negative, will be treated as a limit on number of actions. Optional, defaults to -10.
        :param stop:        Version number to stop listing at. Not the count of actions. Optional, defaults to none.
        :return:            List of dictionaries which describe actions on the filesystem.
        :raises SessionNotLinked:       CloudFSRESTAdapter is not authenticated.
        :raises AuthenticatedError:     Based on CloudFS Error Code.
        """
        params = {
            'start': start
        }

        if stop:
            params['stop'] = stop

        return self._make_request('action history', params=params)


class CloudFSConnection(object):
    def __init__(self, url_root, client_id, secret, auth_token=''):
        super(CloudFSConnection, self).__init__()
        # ignore any formatting the user tries to do
        if url_root.find('http') == 0:
            parsed_url = urlparse(url_root)
            url_root = parsed_url.netloc
        if url_root.find('www') == 0:
            url_root = url_root.replace('www.', '', 1)
        self.url_root = url_root
        self.client_id = client_id
        self.secret = secret
        self.auth_token = auth_token
        self.header_information = {}
        self.debug_one_request = False
        self.threads = []
        self.threads_joined = False
        self.last_request_log = ''

    def __del__(self):
        if not self.threads_joined:
            self.join_threads()

    def debug_next_request(self):
        self.debug_one_request = True

    def join_threads(self, thread_timeout=None):
        all_threads_joined = True
        for thread in self.threads:
            thread.join(thread_timeout)
            all_threads_joined = all_threads_joined and not thread.isAlive()

        self.threads_joined = True

        return all_threads_joined

    def oauth_request(self, path, data={}, params={}, method='GET', current_date=None):
        result = self._request(path, method, data=data, params=params, oauth=True, current_date=current_date)
        if 'access_token' in result:
            self.auth_token = result['access_token']

        return result

    def request(self, path, data={}, params={}, files=None, method='GET', response_processor=None, headers={},
                background=False):
        default_headers = {'Authorization': 'Bearer {}'.format(self.auth_token)}
        if self.auth_token != '':
            default_headers.update(headers)
            result = self._request(path, method, data, default_headers, params, files, response_processor,
                                   background=background)

            if 'result' in result:
                return result['result']
            else:
                return result
        else:
            raise session_not_linked_error()

    @staticmethod
    def _get_base_headers(oauth=False, current_date=None):
        headers = {}
        if oauth:
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset="utf-8"'
        if current_date is not None:
            print "current_date = {}".format(current_date)
            headers['Date'] = current_date
        else:
            headers['Date'] = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        headers['User-Agent'] = 'CloudFSPythonSDK/0.80.2'

        return headers

    # where the magic happens
    def _sign_request(self, method, path, query, headers):

        interesting_headers = ['content-type', 'date']

        def encode_dict_nosort(d, sep):
            encoded_options = []

            for key in d.keys():
                encoded_options.append('{encoded_key}{sep}{encoded_value}'.format(
                    encoded_key=utf8_quote_plus(key),
                    sep=sep,
                    encoded_value=utf8_quote_plus(d[key])
                ))

            return '&'.join(encoded_options)

        def encode_dictionary(d, sep, filter=None):
            dict_to_encode = {}
            sort_keys = {}
            order = []
            encoded_options = []

            if filter != None:
                for key in d.keys():
                    if key.lower() in filter:
                        dict_to_encode[key] = d[key]
            else:
                dict_to_encode = d

            for key in dict_to_encode.keys():
                sort_key = '{}/{}'.format(key.lower(), str(dict_to_encode[key]).lower())
                sort_keys[sort_key] = key

            sorted_keys = sorted(sort_keys.keys())
            for key in sorted_keys:
                order.append(sort_keys[key])

            for key in order:
                encoded_options.append('{encoded_key}{sep}{encoded_value}'.format(
                    encoded_key=utf8_quote_plus(key),
                    sep=sep,
                    encoded_value=utf8_quote_plus(dict_to_encode[key])
                ))

            return '&'.join(encoded_options)

        sig_hmac = hmac.new(make_utf8(self.secret), digestmod=hashlib.sha1)

        print "utf8(secret) = {}".format(make_utf8(self.secret))

        digest = '{method}&{path}&{query}&{headers}'.format(
            method=method,
            path=path,
            query=encode_dictionary(query, '='),
            headers=encode_dictionary(headers, ':', interesting_headers)
        )

        print "digest = {}".format(digest)

        sig_hmac.update(digest)

        signature = base64.encodestring(sig_hmac.digest()).strip()

        headers['Authorization'] = 'BCS {}:{}'.format(self.client_id, signature)

        return headers

    def _save_x_headers(self, headers):
        header_data = {}
        headers_to_parse = [
            # format:
            # outer dict key, header name, inner dict key
            ['storage', 'X-BCS-Account-Storage-Limit', 'limit'],
            ['storage', 'X-BCS-Account-Storage-Usage', 'usage'],
        ]

        for header_info in headers_to_parse:
            if header_info[1] in headers:
                if header_info[0] not in header_data:
                    header_data[header_info[0]] = {}

                header_data[header_info[0]][header_info[2]] = headers[header_info[1]]

                if headers[header_info[1]] == 'None':
                    header_data[header_info[0]][header_info[2]] = None

        self.header_information = header_data

    # must use string or unicode values, as urllib has
    # unpredictable behavior when dealing with objects
    def _filter_arg_dictonary(self, dict):
        from ..path import Path
        filtered_dict = {}
        for k, v in dict.iteritems():
            filtered_key = k
            filtered_value = v

            if type(k) is not str and type(k) is not unicode:
                filtered_key = str(k)
            if type(v) is list and len(v) > 0:
                # if this is all on one line, it will fail to short-circuit
                if hasattr(v[0], 'path') or isinstance(v[0], Path):
                    # allow lists of items
                    filtered_value = [str(item) for item in v]
            else:
                if type(v) is not str and type(v) is not unicode:
                    filtered_value = str(v)
            filtered_dict[filtered_key] = filtered_value

        return filtered_dict

    # TODO: add streaming requests for downloads!
    def _request(self, path, method, data={}, headers={}, params={}, files=None, response_processor=None, oauth=False,
                 background=False, current_date=None):
        single_debug = self.debug_one_request
        self.debug_one_request = False

        data = self._filter_arg_dictonary(data)
        params = self._filter_arg_dictonary(params)
        method = method.upper()
        headers.update(self._get_base_headers(oauth=oauth, current_date=current_date))
        if oauth:
            headers = self._sign_request(method, path, data, headers)

        url = 'https://{}{}'.format(self.url_root, path)

        base_request = requests.Request(method, url, headers, data=data, params=params, files=files)
        prepared_request = base_request.prepare()
        self.prepared_request = 'Prepared_Request:\n{}'.format(request_to_string(prepared_request))
        print "{}".format(self.prepared_request)

        response = requests.Session().send(prepared_request, stream=background)

        self.last_request_log = 'Response:\n{}'.format(request_to_string(prepared_request),
                                                       response_to_string(response))
        print "response status={}".format(response.status_code)

        if response.status_code >= 200 and response.status_code <= 400:
            self._save_x_headers(response.headers)

            if response_processor:
                # clear out old threads if possible
                if background:
                    thread = threading.Thread(target=response_processor, args=(response,))
                    # yolo!
                    thread.start()
                    self.threads.append(thread)
                    # not sure how to clean this up properly.
                else:
                    response_processor(response)

            if 'application/json' in response.headers['Content-Type']:
                return json.loads(response.content)
            else:
                return response.content
        else:
            print "last request log:\n-----------\n{}".format(self.last_request_log)
            raise error_from_response(prepared_request, response)

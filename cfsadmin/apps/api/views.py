"""
Defines the views for API module.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from serializers import BitcasaUserSerializer, BitcasaAccountSerializer, BitcasaAccountStateSerializer, FolderSerializer
from cfsadmin.lib.cloudfs import Session, Path
from cfsadmin.lib.cloudfs_session import UserSession
from cfsadmin.settings.common import CLOUD_FS_SETTINGS
from cfsadmin.lib.cloudfs.private.cloudfs_paths import ExistValues

import json


def _create_session(auth_status=False, auth_key=''):
    """
    Creates CloudFS session depending on the auth_key
    """
    if auth_status:
        cloud_fs_session = UserSession(CLOUD_FS_SETTINGS['API_SERVER'],
                                       CLOUD_FS_SETTINGS['CLIENT_ID'],
                                       CLOUD_FS_SETTINGS['SECRET_KEY'],
                                       auth_key)
    else:
        cloud_fs_session = Session(CLOUD_FS_SETTINGS['API_SERVER'],
                                   CLOUD_FS_SETTINGS['CLIENT_ID'],
                                   CLOUD_FS_SETTINGS['SECRET_KEY'])
    return cloud_fs_session


class User(APIView):
    """
    Handles the POST requests for creating new user accounts.
    """
    response_messages = {
        'invalid_arguments': 'Invalid arguments.',
        'auth_error': 'Unable to authenticate the Bitcasa session.',
        'parse_error': 'Unable to parse given data.',
        'user_created': 'User has been created successfully.'
    }

    def post(self, request, format=None):
        bitcasa_user = BitcasaUserSerializer(data=request.DATA)

        if bitcasa_user.is_valid():
            bitcasa_session = Session(
                CLOUD_FS_SETTINGS['API_SERVER'],
                CLOUD_FS_SETTINGS['CLIENT_ID'],
                CLOUD_FS_SETTINGS['SECRET_KEY'])

            bitcasa_session.set_admin_credentials(CLOUD_FS_SETTINGS['ADMIN_ID'], CLOUD_FS_SETTINGS['ADMIN_SECRET'])

            try:
                user = bitcasa_session.create_account(
                    username=bitcasa_user.data['username'],
                    password=bitcasa_user.data['password'],
                    first_name=bitcasa_user.data['first_name'],
                    last_name=bitcasa_user.data['last_name'],
                    account_plan_uuid=bitcasa_user.data['account_plan_uuid'],
                    current_date=bitcasa_user.data['current_date'],
                    tkey=True, debug=True)

                return Response(
                    {'user': user.data,
                     'success': True,
                     'message': self.response_messages['user_created']},
                    status=status.HTTP_201_CREATED)

            except Exception as exc:
                r = json.loads(exc.response.content)
                return Response(
                    {'success': False,
                     'message': str(r['message'])},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            message = self.response_messages['invalid_arguments'] + ' '

            for key in bitcasa_user.errors:
                message += key + ' : '
                for m in bitcasa_user.errors[key]:
                    message += str(m)

                message += ' '

            return Response(
                {'success': False, 'message': message},
                status=status.HTTP_400_BAD_REQUEST)


class Authenticate(APIView):
    response_messages = {
        'invalid_arguments': 'Invalid arguments.',
        'auth_error': 'Unable to authenticate the Bitcasa session.',
        'parse_error': 'Unable to parse given data.',
        'auth_token_generated': 'Auth token generated successfully.'
    }

    def post(self, request, format=None):
        bitcasa_account = BitcasaAccountSerializer(data=request.DATA)
        if bitcasa_account.is_valid():
            bitcasa_session = Session(
                CLOUD_FS_SETTINGS['API_SERVER'],
                CLOUD_FS_SETTINGS['CLIENT_ID'],
                CLOUD_FS_SETTINGS['SECRET_KEY'])

            try:
                authenticated = bitcasa_session.authenticate(bitcasa_account.data['username'],
                                                             bitcasa_account.data['password'])
                auth_token = bitcasa_session.rest_interface.bc_conn.auth_token
                if authenticated:
                    msg = self.response_messages['auth_token_generated']
                else:
                    msg = self.response_messages['auth_error']

                return Response(
                    {'auth_token': auth_token,
                     'success': authenticated,
                     'message': msg},
                    status=status.HTTP_200_OK)
            except Exception as exc:
                print "exception caught"
                r = json.loads(exc.response.content)
                return Response(
                    {'success': False,
                     'message': str(r['message'])},
                    status=status.HTTP_400_BAD_REQUEST)

        else:
            message = self.response_messages['invalid_arguments'] + ' '
            for key in bitcasa_account.errors:
                message += key + ' : '
                for m in bitcasa_account.errors[key]:
                    message += str(m)

                message += ' '

            return Response(
                {'success': False, 'message': message},
                status=status.HTTP_400_BAD_REQUEST)


class AccountState(APIView):
    """
    Handles the POST requests for accountState
    """
    response_messages = {
        'invalid_arguments': 'Invalid arguments.',
        'auth_error': 'Unable to authenticate the Bitcasa session.',
        'parse_error': 'Unable to parse given data.',
        'user_updated': 'User has been updated successfully.'
    }

    def post(self, request, format=None):
        bitcasa_account_state = BitcasaAccountStateSerializer(data=request.DATA)

        if bitcasa_account_state.is_valid():
            bitcasa_session = Session(
                CLOUD_FS_SETTINGS['API_SERVER'],
                CLOUD_FS_SETTINGS['CLIENT_ID'],
                CLOUD_FS_SETTINGS['SECRET_KEY'])

            bitcasa_session.set_admin_credentials(CLOUD_FS_SETTINGS['ADMIN_ID'], CLOUD_FS_SETTINGS['ADMIN_SECRET'])

            try:
                print "calling AccountState on user_id={}".format(bitcasa_account_state.data['user_id'])

                state = bitcasa_session.account_state(
                    user_id=bitcasa_account_state.data['user_id'],
                    first_name=bitcasa_account_state.data['first_name'],
                    last_name=bitcasa_account_state.data['last_name'],
                    plan_code=bitcasa_account_state.data['plan_code'],
                    expiration_date=bitcasa_account_state.data['expiration_date'],
                    grace=bitcasa_account_state.data['grace'],
                    ignore_otl=bitcasa_account_state.data['ignore_otl'],
                    plan_transition=bitcasa_account_state.data['plan_transition'],
                    debug=True
                )

                print "account state done"

                return Response(
                    {'AccountState': state,
                     'success': True,
                     'message': self.response_messages['user_updated']},
                    status=status.HTTP_200_OK)

            except Exception as exc:
                r = json.loads(exc.response.content)
                return Response(
                    {'success': False,
                     'message': str(r['message'])},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            message = self.response_messages['invalid_arguments'] + ' '

            for key in bitcasa_account_state.errors:
                message += key + ' : '
                for m in bitcasa_account_state.errors[key]:
                    message += str(m)

                message += ' '

            return Response(
                {'success': False, 'message': message},
                status=status.HTTP_400_BAD_REQUEST)


class Delete(APIView):
    """
    Handles the POST requests for deleting user accounts.
    """
    response_messages = {
        'invalid_arguments': 'Invalid arguments.',
        'auth_error': 'Unable to authenticate the Bitcasa session.',
        'parse_error': 'Unable to parse given data.',
        'user_deleted': 'User has been successfully deleted.'
    }

    def post(self, request, format=None):
        bitcasa_account_state = BitcasaAccountStateSerializer(data=request.DATA)

        if bitcasa_account_state.is_valid():
            bitcasa_session = Session(
                CLOUD_FS_SETTINGS['API_SERVER'],
                CLOUD_FS_SETTINGS['CLIENT_ID'],
                CLOUD_FS_SETTINGS['SECRET_KEY'])

            bitcasa_session.set_admin_credentials(CLOUD_FS_SETTINGS['ADMIN_ID'], CLOUD_FS_SETTINGS['ADMIN_SECRET'])

            try:
                response = bitcasa_session.delete_account(user_id=bitcasa_account_state.data['user_id'], debug=True)

                return Response(
                    {'result': response,
                     'success': True,
                     'message': self.response_messages['user_deleted']},
                    status=status.HTTP_200_OK)

            except Exception as exc:
                r = json.loads(exc.response.content)
                return Response(
                    {'success': False,
                     'message': str(r['message'])},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            message = self.response_messages['invalid_arguments'] + ' '

            for key in bitcasa_account_state.errors:
                message += key + ' : '
                for m in bitcasa_account_state.errors[key]:
                    message += str(m)

                message += ' '

            return Response(
                {'success': False, 'message': message},
                status=status.HTTP_400_BAD_REQUEST
            )


class FolderCreate(APIView):
    response_messages = {
        'invalid_arguments': 'Invalid arguments.',
        'auth_error': 'Unable to authenticate the Bitcasa session.',
        'parse_error': 'Unable to parse given data.',
        'unauthenticated': 'Unauthenticated'
    }

    @staticmethod
    def container_from_path(container, name):
        children = container.list()
        for item in children:
            print "...{}.{}".format(container.name, item.name)
            if item.name == name:
                return item
        return container

    def post(self, request):
        folder_creator = FolderSerializer(data=request.DATA)

        if folder_creator.is_valid():
            bc_session = Session(
                CLOUD_FS_SETTINGS['API_SERVER'],
                CLOUD_FS_SETTINGS['CLIENT_ID'],
                CLOUD_FS_SETTINGS['SECRET_KEY'])

            try:
                authenticated = bc_session.authenticate(folder_creator.data['username'],
                                                        folder_creator.data['password'])

                if authenticated:
                    bearer_auth = bc_session.rest_interface.bc_conn.auth_token
                    user_session = UserSession(CLOUD_FS_SETTINGS['API_SERVER'],
                                               CLOUD_FS_SETTINGS['CLIENT_ID'],
                                               CLOUD_FS_SETTINGS['SECRET_KEY'],
                                               bearer_auth)

                    user_session.rest_interface.debug_requests(1)
                    file_system = user_session.get_filesystem()
                    root_folder = file_system.root_container()

                    try:
                        target_folder = root_folder

                        if folder_creator.data['path'] is not None:
                            paths = folder_creator.data['path']
                            path_list = paths.split('/')
                            for path_item in path_list:
                                target_folder = self.container_from_path(target_folder, path_item)

                        print "going to create a folder named '{}' in my {} directory...".format(folder_creator.data['name'], target_folder.name)
                        target_folder.create_folder(container_or_name=folder_creator.data['name'], exists=ExistValues.overwrite, debug=False)

                    except Exception as exc:
                        r = json.loads(exc.response.content)
                        return Response(
                            {'success': False,
                             'message': str(r['message'])},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    return Response({'success': True},
                                    status=status.HTTP_201_CREATED
                                    )

                else:
                    return Response({'success': False},
                                    status=status.HTTP_401_UNAUTHORIZED
                                    )

            except Exception as exc:
                r = json.loads(exc.response.content)
                return Response(
                    {'success': False,
                     'message': str(r['message'])},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            message = self.response_messages['invalid_arguments'] + ' '

            for key in folder_creator.errors:
                message += key + ' : '
                for m in folder_creator.errors[key]:
                    message += str(m)

                message += ' '

            return Response(
                {'success': False, 'message': message},
                status=status.HTTP_400_BAD_REQUEST)


class FolderDelete(APIView):
    response_messages = {
        'invalid_arguments': 'Invalid arguments.',
        'auth_error': 'Unable to authenticate the Bitcasa session.',
        'parse_error': 'Unable to parse given data.',
        'unauthenticated': 'Unauthenticated'
    }

    def post(self, request):
        folder_creator = FolderSerializer(data=request.DATA)

        if folder_creator.is_valid():
            bc_session = Session(
                CLOUD_FS_SETTINGS['API_SERVER'],
                CLOUD_FS_SETTINGS['CLIENT_ID'],
                CLOUD_FS_SETTINGS['SECRET_KEY'])

            try:
                authenticated = bc_session.authenticate(folder_creator.data['username'],
                                                        folder_creator.data['password'])

                if authenticated:
                    bearer_auth = bc_session.rest_interface.bc_conn.auth_token
                    user_session = UserSession(CLOUD_FS_SETTINGS['API_SERVER'],
                                               CLOUD_FS_SETTINGS['CLIENT_ID'],
                                               CLOUD_FS_SETTINGS['SECRET_KEY'],
                                               bearer_auth)

                    user_session.rest_interface.debug_requests(1)
                    print "got a user session"

                    file_system = user_session.get_filesystem()
                    root_folder = file_system.root_container()

                    try:
                        root_list = root_folder.list()
                        for root_item in root_list:
                            print "before: {}".format(root_item.name)

                        print "going to delete a folder named '{}' in my root directory...".format(folder_creator.data['name'])
                        for root_item in root_list:
                            if root_item.name == folder_creator.data['name']:
                                print "deleting '{}'".format(folder_creator.data['name'])
                                root_item.delete(commit=True, force=True, debug=True)

                        root_list = root_folder.list()
                        for root_item in root_list:
                            print "after: {}".format(root_item.name)

                    except Exception as exc:
                        r = json.loads(exc.response.content)
                        return Response(
                            {'success': False,
                             'message': str(r['message'])},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    return Response({'success': True},
                                    status=status.HTTP_200_OK
                                    )

                else:
                    return Response({'success': False},
                                    status=status.HTTP_401_UNAUTHORIZED
                                    )

            except Exception as exc:
                r = json.loads(exc.response.content)
                return Response(
                    {'success': False,
                     'message': str(r['message'])},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            message = self.response_messages['invalid_arguments'] + ' '

            for key in folder_creator.errors:
                message += key + ' : '
                for m in folder_creator.errors[key]:
                    message += str(m)

                message += ' '

            return Response(
                {'success': False, 'message': message},
                status=status.HTTP_400_BAD_REQUEST)

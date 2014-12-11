"""
Defines the views for API module.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from serializers import BitcasaUserSerializer, BitcasaAccountSerializer
from signup.lib.cloudfs import UnknownError
from signup.lib.cloudfs import Session, OperationNotAllowed
from signup.settings.common import CLOUD_FS_SETTINGS
import json


class User(APIView):
    """
    Handles the POST requests for creating new user accounts.
    """
    response_messages = {
        'invalid_arguments' : 'Invalid arguments.',
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
                    bitcasa_user.data['username'],
                    bitcasa_user.data['password'],
                    bitcasa_user.data['first_name'],
                    bitcasa_user.data['last_name'])

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
                {'success': False,'message': message},
                status=status.HTTP_400_BAD_REQUEST)


class Authenticate(APIView):
    response_messages = {
        'invalid_arguments' : 'Invalid arguments.',
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
                bitcasa_session.authenticate(bitcasa_account.data['username'], bitcasa_account.data['password'])
                auth_token = bitcasa_session.rest_interface.bc_conn.auth_token
                return Response(
                    {'auth_token': auth_token,
                     'success': True,
                     'message': self.response_messages['auth_token_generated']},
                    status=status.HTTP_200_OK)
            except Exception as exc:
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
                {'success': False,'message': message},
                status=status.HTTP_400_BAD_REQUEST)

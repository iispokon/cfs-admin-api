"""
Defines the serializer classes for API module.
"""
from rest_framework import serializers


class BitcasaUser(object):
    """
    Object that represents a Bitcasa User.
    """

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name


class BitcasaAccount(object):
    """
    Defines bitcasa cloudFS account details.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password


class BitcasaUserSerializer(serializers.Serializer):
    """
    The Serializer class for BitcasaUser object.
    """
    username = serializers.CharField(max_length=100, blank=False)
    password = serializers.CharField(max_length=100, blank=False)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            instance.username = attrs.get('username', instance.username)
            instance.password = attrs.get('password', instance.password)
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.last_name = attrs.get('last_name', instance.last_name)
            return instance

        return BitcasaUser(**attrs)


class BitcasaAccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, blank=False)
    password = serializers.CharField(max_length=100, blank=False)

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of field values, either updates or creates a Account instance.
        """
        if instance is not None:
            instance.username = attrs.get('username', instance.username)
            instance.password = attrs.get('password', instance.password)
            return instance

        return BitcasaAccount(**attrs)
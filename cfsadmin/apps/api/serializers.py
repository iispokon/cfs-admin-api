"""
Defines the serializer classes for API module.
"""
from rest_framework import serializers


class BitcasaUser(object):
    """
    Object that represents a Bitcasa User.
    """

    def __init__(self, username, password, first_name=None, last_name=None, account_plan_uuid=None, current_date=None):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.account_plan_uuid = account_plan_uuid
        self.current_date = current_date


class BitcasaAccountState(object):
    def __init__(self, user_id, username=None, first_name=None, last_name=None, plan_code=None,
                 expiration_date=None, grace=None, ignore_otl=None, plan_transition=None):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.plan_code = plan_code
        self.expiration_date = expiration_date
        self.grace = grace
        self.ignore_otl = ignore_otl
        self.plan_transition = plan_transition


class BitcasaAccount(object):
    """
    Defines bitcasa cloudFS account details.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Folder(object):
    def __init__(self, username, password, name, path=None):
        self.username = username
        self.password = password
        self.path = path
        self.name = name


class BitcasaUserSerializer(serializers.Serializer):
    """
    The Serializer class for BitcasaUser object.
    """
    username = serializers.CharField(max_length=100, blank=False)
    password = serializers.CharField(max_length=100, blank=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    account_plan_uuid = serializers.CharField(max_length=200, required=False)
    current_date = serializers.CharField(max_length=100, required=False)

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
            instance.account_plan_uuid = attrs.get('account_plan_uuid', instance.account_plan_uuid)
            instance.current_date = attrs.get('current_date', instance.current_date)
            return instance

        return BitcasaUser(**attrs)


class BitcasaAccountStateSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, blank=False)
    username = serializers.CharField(max_length=100, required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    plan_code = serializers.CharField(max_length=200, required=False)
    expiration_date = serializers.CharField(max_length=14, required=False)
    grace = serializers.CharField(max_length=5, required=False)
    ignore_otl = serializers.CharField(max_length=5, required=False)
    plan_transition = serializers.CharField(max_length=100, required=False)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.user_id = attrs.get('user_id', instance.user_id)
            instance.username = attrs.get('username', instance.username)
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.last_name = attrs.get('last_name', instance.last_name)
            instance.plan_code = attrs.get('plan_code', instance.plan_code)
            instance.expiration_date = attrs.get('expiration_date', instance.expiration_date)
            instance.sunset = attrs.get('grace', instance.grace)
            instance.ignore_otl = attrs.get('ignore_otl', instance.ignore_otl)
            instance.plan_transition = attrs.get('plan_transition', instance.plan_transition)
            return instance

        return BitcasaAccountState(**attrs)


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


class FolderSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, blank=False)
    password = serializers.CharField(max_length=100, blank=False)
    name = serializers.CharField(blank=False)
    path = serializers.CharField(required=False)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.username = attrs.get('username', instance.username)
            instance.password = attrs.get('password', instance.password)
            instance.name = attrs.get('name', instance.name)
            instance.path = attrs.get('path', instance.path)
            return instance

        return Folder(**attrs)

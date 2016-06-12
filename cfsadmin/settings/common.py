"""
Django settings for signup project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8a7e%tx%+*vx49y2s!qz%fvu!cbf)s+oond3y5wdc&hvw5pymr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'cfsadmin.apps.api',
)

MIDDLEWARE_CLASSES = (
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cfsadmin.urls'

WSGI_APPLICATION = 'cfsadmin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {}

# Test runner will not set up and tear down a database.
TEST_RUNNER = 'testing.DatabaselessTestRunner'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


def abs_path(*args):
    r"""
    Convert project relative path to absolute path.
    :param list \*args: Path fragments that should be concatenated.
    :returns: The absolute path.
    """
    return os.path.join(ROOT_DIR, *args)

STATIC_ROOT = abs_path('staticfiles')

# Additional locations of static files
STATICFILES_DIRS = (
    abs_path('static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


api_server = {'cfs':'yna65xy5kb.cloudfs.io',
              '3-Denmark':'sdext-access.cloudfs.io',
              'Indosat':'sdext-access.cloudfs.io',
              'Ooredoo Qatar':'sdext-access.cloudfs.io',
              'Ooredoo Qatar API':'ooredoo-qa.api.sandbox.cloudfs.io',
              'Zain Jordan':'sdext-access.cloudfs.io'
              }
client_id = {'cfs':'wA-5oH1g6maFTldWxqb6fQxo_5sJEDKyPqN_kLiHfgo',
             '3-Denmark':'TWUI9e1Vg7uEvv3-JDiEi4Xf5JCihPfftNvcjrnXiZQ',
             'Indosat':'qqibtTQqwJVnWyaZ0s3Jfux4YpDXDOF7YsULoUwf5oo',
             'Ooredoo Qatar':'zCrYKyrOevDlqhDB2SpfcJ0-TlRJQa2LAggNmeG_2jQ',
             'Ooredoo Qatar API':'4FxyBunuA-aYzzTKZTN6L8Z20TcPO3hAHAH7-nrqE4c',
             'Zain Jordan':'y3T3XT7yrdVEQSGbqRHXpqK6nyaG_MFZ78AZtGR4A4M'
             }
secret_key = {'cfs':'MiGpSaLxuryHAr_t2Yvd_q3tna9khvYHehuz_SOgH_uvBQBL69Aj3lc_nZenSArbsJatjyHIZ_C7WdkCmn7eUQ',
              '3-Denmark':'rZBQsgCJWJxmS563Q299k7GbG-vDX56Zb6JBydN1FdfjHaMo1YvcJ3kfVfy03CdwxrcrVDYLLBj9w8rOZ3EUkA',
              'Indosat':'6Ug9RgPjaaQyvAKdCjpPtDnheCbqqoXbDSsLM7ir-ldIPpjz3sAHmbz_sTqZP6n9pWcuqpbD-cD4ntwqVQRjKw',
              'Ooredoo Qatar':'1ou4t1Z6gqIq9PH7Mp3pq4-oNYoKN3PKx91r_NGdfdozW9tM7twG1f3NyFSYq6V6KV1E7eiCTJTNsNMnj7BJ3A',
              'Ooredoo Qatar API':'yBGvyIkvKOwdQxi7gHwxM1x6d9HbDBeeIJjaWHmQsEkvm4NBCC5EaERgwaY4FD0onuzdMZQpJohChS4-wpYzrQ',
              'Zain Jordan':'kpd9QYVRma_Zn4GfKfHd1uqX-cWKjLlDwKzjPehtjkCF7vR3tRXfm1LAABGYT0yE_WgBZ-LPcN4Oo8qSmG4NpQ'
              }
admin_id = {'cfs':'wA-5oH1g6maFTldWxqb6fQxo_5sJEDKyPqN_kLiHfgo',
            '3-Denmark':'TWUI9e1Vg7uEvv3-JDiEi4Xf5JCihPfftNvcjrnXiZQ',
            'Indosat':'qqibtTQqwJVnWyaZ0s3Jfux4YpDXDOF7YsULoUwf5oo',
            'Ooredoo Qatar':'zCrYKyrOevDlqhDB2SpfcJ0-TlRJQa2LAggNmeG_2jQ',
            'Ooredoo Qatar API':'4FxyBunuA-aYzzTKZTN6L8Z20TcPO3hAHAH7-nrqE4c',
            'Zain Jordan':'y3T3XT7yrdVEQSGbqRHXpqK6nyaG_MFZ78AZtGR4A4M'
            }
admin_secret = {'cfs':'MiGpSaLxuryHAr_t2Yvd_q3tna9khvYHehuz_SOgH_uvBQBL69Aj3lc_nZenSArbsJatjyHIZ_C7WdkCmn7eUQ',
                '3-Denmark':'rZBQsgCJWJxmS563Q299k7GbG-vDX56Zb6JBydN1FdfjHaMo1YvcJ3kfVfy03CdwxrcrVDYLLBj9w8rOZ3EUkA',
                'Indosat':'6Ug9RgPjaaQyvAKdCjpPtDnheCbqqoXbDSsLM7ir-ldIPpjz3sAHmbz_sTqZP6n9pWcuqpbD-cD4ntwqVQRjKw',
                'Ooredoo Qatar':'1ou4t1Z6gqIq9PH7Mp3pq4-oNYoKN3PKx91r_NGdfdozW9tM7twG1f3NyFSYq6V6KV1E7eiCTJTNsNMnj7BJ3A',
                'Ooredoo Qatar API':'yBGvyIkvKOwdQxi7gHwxM1x6d9HbDBeeIJjaWHmQsEkvm4NBCC5EaERgwaY4FD0onuzdMZQpJohChS4-wpYzrQ',
                'Zain Jordan':'kpd9QYVRma_Zn4GfKfHd1uqX-cWKjLlDwKzjPehtjkCF7vR3tRXfm1LAABGYT0yE_WgBZ-LPcN4Oo8qSmG4NpQ'
                }

env = 'Zain Jordan'


CLOUD_FS_SETTINGS = {
    'API_SERVER': api_server[env],
    'CLIENT_ID':  client_id[env],
    'SECRET_KEY': secret_key[env],
    'ADMIN_ID':   admin_id[env],
    'ADMIN_SECRET': admin_secret[env]
}


# #cfs
# CLOUD_FS_SETTINGS = {
#     'API_SERVER': 'yna65xy5kb.cloudfs.io',
#     'CLIENT_ID':    'wA-5oH1g6maFTldWxqb6fQxo_5sJEDKyPqN_kLiHfgo',
#     'SECRET_KEY':   'MiGpSaLxuryHAr_t2Yvd_q3tna9khvYHehuz_SOgH_uvBQBL69Aj3lc_nZenSArbsJatjyHIZ_C7WdkCmn7eUQ',
#     'ADMIN_ID':     'wA-5oH1g6maFTldWxqb6fQxo_5sJEDKyPqN_kLiHfgo',
#     'ADMIN_SECRET': 'MiGpSaLxuryHAr_t2Yvd_q3tna9khvYHehuz_SOgH_uvBQBL69Aj3lc_nZenSArbsJatjyHIZ_C7WdkCmn7eUQ'
# }

# #3-Denmark
# CLOUD_FS_SETTINGS = {
#     'API_SERVER': 'sdext-access.cloudfs.io',
#     'CLIENT_ID': 'TWUI9e1Vg7uEvv3-JDiEi4Xf5JCihPfftNvcjrnXiZQ',
#     'SECRET_KEY': 'rZBQsgCJWJxmS563Q299k7GbG-vDX56Zb6JBydN1FdfjHaMo1YvcJ3kfVfy03CdwxrcrVDYLLBj9w8rOZ3EUkA',
#     'ADMIN_ID': 'TWUI9e1Vg7uEvv3-JDiEi4Xf5JCihPfftNvcjrnXiZQ',
#     'ADMIN_SECRET': 'rZBQsgCJWJxmS563Q299k7GbG-vDX56Zb6JBydN1FdfjHaMo1YvcJ3kfVfy03CdwxrcrVDYLLBj9w8rOZ3EUkA'
# }

# #Indosat
# CLOUD_FS_SETTINGS = {
#     'API_SERVER': 'sdext-access.cloudfs.io',
#     'CLIENT_ID': 'qqibtTQqwJVnWyaZ0s3Jfux4YpDXDOF7YsULoUwf5oo',
#     'SECRET_KEY': '6Ug9RgPjaaQyvAKdCjpPtDnheCbqqoXbDSsLM7ir-ldIPpjz3sAHmbz_sTqZP6n9pWcuqpbD-cD4ntwqVQRjKw',
#     'ADMIN_ID': 'qqibtTQqwJVnWyaZ0s3Jfux4YpDXDOF7YsULoUwf5oo',
#     'ADMIN_SECRET': '6Ug9RgPjaaQyvAKdCjpPtDnheCbqqoXbDSsLM7ir-ldIPpjz3sAHmbz_sTqZP6n9pWcuqpbD-cD4ntwqVQRjKw'
# }

# #Ooredoo Qatar
# CLOUD_FS_SETTINGS = {
#     'API_SERVER': 'sdext-access.cloudfs.io',
#     'CLIENT_ID':    'zCrYKyrOevDlqhDB2SpfcJ0-TlRJQa2LAggNmeG_2jQ',
#     'SECRET_KEY':   '1ou4t1Z6gqIq9PH7Mp3pq4-oNYoKN3PKx91r_NGdfdozW9tM7twG1f3NyFSYq6V6KV1E7eiCTJTNsNMnj7BJ3A',
#     'ADMIN_ID':     'zCrYKyrOevDlqhDB2SpfcJ0-TlRJQa2LAggNmeG_2jQ',
#     'ADMIN_SECRET': '1ou4t1Z6gqIq9PH7Mp3pq4-oNYoKN3PKx91r_NGdfdozW9tM7twG1f3NyFSYq6V6KV1E7eiCTJTNsNMnj7BJ3A'
# }

# #Ooredoo Qatar API
# CLOUD_FS_SETTINGS = {
#     'API_SERVER': 'ooredoo-qa.api.sandbox.cloudfs.io',
#     'CLIENT_ID':    '4FxyBunuA-aYzzTKZTN6L8Z20TcPO3hAHAH7-nrqE4c',
#     'SECRET_KEY':   'yBGvyIkvKOwdQxi7gHwxM1x6d9HbDBeeIJjaWHmQsEkvm4NBCC5EaERgwaY4FD0onuzdMZQpJohChS4-wpYzrQ',
#     'ADMIN_ID':     '4FxyBunuA-aYzzTKZTN6L8Z20TcPO3hAHAH7-nrqE4c',
#     'ADMIN_SECRET': 'yBGvyIkvKOwdQxi7gHwxM1x6d9HbDBeeIJjaWHmQsEkvm4NBCC5EaERgwaY4FD0onuzdMZQpJohChS4-wpYzrQ'
# }

# #Zain Jordan
# CLOUD_FS_SETTINGS = {
#     'API_SERVER': 'sdext-access.cloudfs.io',
#     'CLIENT_ID':    'y3T3XT7yrdVEQSGbqRHXpqK6nyaG_MFZ78AZtGR4A4M',
#     'SECRET_KEY':   'kpd9QYVRma_Zn4GfKfHd1uqX-cWKjLlDwKzjPehtjkCF7vR3tRXfm1LAABGYT0yE_WgBZ-LPcN4Oo8qSmG4NpQ',
#     'ADMIN_ID':     'y3T3XT7yrdVEQSGbqRHXpqK6nyaG_MFZ78AZtGR4A4M',
#     'ADMIN_SECRET': 'kpd9QYVRma_Zn4GfKfHd1uqX-cWKjLlDwKzjPehtjkCF7vR3tRXfm1LAABGYT0yE_WgBZ-LPcN4Oo8qSmG4NpQ'
# }


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
    'signup.apps.api',
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

ROOT_URLCONF = 'signup.urls'

WSGI_APPLICATION = 'signup.wsgi.application'


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


"""
#3-Denmark
CLOUD_FS_SETTINGS = {
    'API_SERVER': 'sdext-access.cloudfs.io',
    'CLIENT_ID': 'TWUI9e1Vg7uEvv3-JDiEi4Xf5JCihPfftNvcjrnXiZQ',
    'SECRET_KEY': 'rZBQsgCJWJxmS563Q299k7GbG-vDX56Zb6JBydN1FdfjHaMo1YvcJ3kfVfy03CdwxrcrVDYLLBj9w8rOZ3EUkA',
    'ADMIN_ID': 'TWUI9e1Vg7uEvv3-JDiEi4Xf5JCihPfftNvcjrnXiZQ',
    'ADMIN_SECRET': 'rZBQsgCJWJxmS563Q299k7GbG-vDX56Zb6JBydN1FdfjHaMo1YvcJ3kfVfy03CdwxrcrVDYLLBj9w8rOZ3EUkA'
}
"""

#Indosat
CLOUD_FS_SETTINGS = {
    'API_SERVER': 'sdext-access.cloudfs.io',
    'CLIENT_ID': 'qqibtTQqwJVnWyaZ0s3Jfux4YpDXDOF7YsULoUwf5oo',
    'SECRET_KEY': '6Ug9RgPjaaQyvAKdCjpPtDnheCbqqoXbDSsLM7ir-ldIPpjz3sAHmbz_sTqZP6n9pWcuqpbD-cD4ntwqVQRjKw',
    'ADMIN_ID': 'qqibtTQqwJVnWyaZ0s3Jfux4YpDXDOF7YsULoUwf5oo',
    'ADMIN_SECRET': '6Ug9RgPjaaQyvAKdCjpPtDnheCbqqoXbDSsLM7ir-ldIPpjz3sAHmbz_sTqZP6n9pWcuqpbD-cD4ntwqVQRjKw'
}

"""
#Ooredoo Qatar
CLOUD_FS_SETTINGS = {
    'API_SERVER': 'sdext-access.cloudfs.io',
    'CLIENT_ID':    'zCrYKyrOevDlqhDB2SpfcJ0-TlRJQa2LAggNmeG_2jQ',
    'SECRET_KEY':   '1ou4t1Z6gqIq9PH7Mp3pq4-oNYoKN3PKx91r_NGdfdozW9tM7twG1f3NyFSYq6V6KV1E7eiCTJTNsNMnj7BJ3A',
    'ADMIN_ID':     'zCrYKyrOevDlqhDB2SpfcJ0-TlRJQa2LAggNmeG_2jQ',
    'ADMIN_SECRET': '1ou4t1Z6gqIq9PH7Mp3pq4-oNYoKN3PKx91r_NGdfdozW9tM7twG1f3NyFSYq6V6KV1E7eiCTJTNsNMnj7BJ3A'
}"""

"""
#Zain Jordan
CLOUD_FS_SETTINGS = {
    'API_SERVER': 'sdext-access.cloudfs.io',
    'CLIENT_ID':    'y3T3XT7yrdVEQSGbqRHXpqK6nyaG_MFZ78AZtGR4A4M',
    'SECRET_KEY':   'kpd9QYVRma_Zn4GfKfHd1uqX-cWKjLlDwKzjPehtjkCF7vR3tRXfm1LAABGYT0yE_WgBZ-LPcN4Oo8qSmG4NpQ',
    'ADMIN_ID':     'y3T3XT7yrdVEQSGbqRHXpqK6nyaG_MFZ78AZtGR4A4M',
    'ADMIN_SECRET': 'kpd9QYVRma_Zn4GfKfHd1uqX-cWKjLlDwKzjPehtjkCF7vR3tRXfm1LAABGYT0yE_WgBZ-LPcN4Oo8qSmG4NpQ'
}"""
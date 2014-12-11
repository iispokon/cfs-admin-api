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

ALLOWED_HOSTS = []


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

CLOUD_FS_SETTINGS = {
    'API_SERVER': 'xk09pv9fc5.cloudfs.io',
    'CLIENT_ID': 'bJ9tTcy2DnvBbF7hJ2j_MSEgfDJ5wXmrN9QcJh04e7A',
    'SECRET_KEY': '1y5U1eIVhW4SHonquOCtzbpNotM6wd7OUTFOwMcEIjpBs20i92P26Aa0Df_67CzsXxXZcoirM9ogJ48HmlMULQ',
    'ADMIN_ID': 'WjibAbRNxBIkxPF5MwLnb_sgB78oZ7H2fHONi0OQdno',
    'ADMIN_SECRET': 'eXbF2B1HKAw8_GwP77JEKsNvATHqChR0r6UYj9uD8wDHL3XCYdpisFtoZgBlnXwTf0NT-74vOPNK06Tgub_cyQ'
}

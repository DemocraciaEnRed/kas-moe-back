# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""Global settings for the project."""

import typing

from pydantic import BaseSettings
from pydantic import Field

from .defs import LogLevel
from .defs import base_dir
from .defs import package_name

# Set the environment prefix
ENV_PREFIX = 'MOE_'


# Configure your settings below. Any business logic or check that you need to apply
# after settings are parsed, do it so in `checks.py`.
class Settings(BaseSettings):
    """Settings for the app."""

    class Config:
        """Configurations for Pydantic settings class."""

        env_prefix = ENV_PREFIX
        env_file = '.env'
        use_enum_values = True

    # Points to the application root directory
    BASE_DIR: str = Field(
        base_dir,
        env=None,
    )

    # Set the package name
    PACKAGE_NAME: str = Field(
        package_name,
        env=None,
    )

    # Development mode: this mode sets several default settings for development.
    # enables debug, sets log level to debug, enables static file server.
    DEVELOPMENT_MODE: bool = Field(False)

    # App title and description shown in open API documentation
    APP_TITLE: str = Field(
        package_name,
        min_length=1,
    )
    APP_DESCRIPTION: str = Field(
        '',
    )

    # Application identifier such as when in a cluster (it's world readable!)
    APP_IDENTIFIER: str = Field(
        package_name,
        min_length=1,
    )

    # Prefix for your API, such as /api/app or /app (must begin with slash)
    API_PREFIX: str = Field(
        '',
        regex=r'(^\/.+?[^\/]$)?',
    )

    # Misc URLs (must begin with slash)
    OPENAPI_URL_PATH: str = Field(
        '/openapi.json',
        regex=r'^\/.+?[^\/]$',
        min_length=1,
    )
    DOCS_URL_PATH: str = Field(
        '/docs',
        regex=r'^\/.+?[^\/]$',
        min_length=1,
    )
    REDOC_URL_PATH: str = Field(
        '/redoc',
        regex=r'^\/.+?[^\/]$',
        min_length=1,
    )
    STATIC_URL_PATH: str = Field(
        '/static',
        regex=r'^\/.+?[^\/]$',
        min_length=1,
    )

    # Application allowed hosts: used to check the Host header and CORS. The first
    # one is considered the main one.
    ALLOWED_HOSTS: typing.List[str] = Field(...)

    # Application allowed origins for CORS configuration. This value is set later
    # on using allowed hosts in `checks.py`.
    ALLOWED_ORIGINS: typing.List[str] = Field(
        [],
        env=None,
    )

    # Debug
    DEBUG: bool = Field(False)

    # Logging
    LOGLEVEL: LogLevel = Field(LogLevel.INFO)

    # Redirect http requests to a secure connection
    ENABLE_HTTPS_REDIRECT: bool = Field(True)

    # External static URL for serving statics (must be a complete URL,
    # including protocol, FQDN and path, ending without slash). This setting
    # overrides STATIC_URL_PATH.
    STATIC_URL: str = Field(
        '',
        regex=r'(^(http[s]?:)?\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F]'
              r'[0-9a-fA-F]))+[^\/]$)?',
    )

    # Allow CORS for a local frontend running in port 3000 (thus the rule is
    # http://127.0.0.1:3000).
    # Defaults to true for development mode, false otherwise.
    ALLOW_FRONTEND_LOCAL: bool = Field(False)

    # Database settings
    DATABASE_DIALECT: str = Field(  # actually its dialect+driver
        'cockroachdb',  # 'postgresql', 'mysql', ...
        min_length=3,
    )
    DATABASE_NAME: str = Field(
        'db.sqlite3',
        min_length=1,
    )
    DATABASE_USER: str = Field('')
    DATABASE_PASSWORD: str = Field('')
    DATABASE_HOST: str = Field(
        '127.0.0.1',
        min_length=1,
    )
    DATABASE_PORT: int = Field(
        26257,
        gt=0,
        lt=65535,
    )
    DATABASE_PARAMS: str = Field('')
    DATABASE_URI: str = Field(  # Populated at `checks.py`
        '',
        env=None,
    )

    # Configure Python logger
    LOGGING: dict = Field(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format':
                        '{levelname} {asctime} p:{process:d} t:{thread:d} '
                        '[{name}.{funcName}:{lineno:d}] {message}',
                    'style': '{',
                },
                'simple': {
                    'format': '{levelname} {asctime} {message}',
                    'datefmt': '%Y-%m-%d %H:%M:%S',
                    'style': '{',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                },
            },
            'loggers': {
                package_name: {
                    'handlers': ['console'],
                    'level': '',  # This value is set afterwards at `configs.py`
                },
            },
        },
    )

    # Define whether we are in a testing environment or not.
    # If this value is True then settings for tests will be loaded.
    TESTING: bool = Field(False)

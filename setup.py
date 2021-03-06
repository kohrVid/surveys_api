from setuptools import setup, find_packages
from decouple import config

setup(
        name= config('APP_NAME'),
        version=config('VERSION'),
        description=config('DESCRIPTION'),
        author=config('AUTHOR'),
        author_email=config('AUTHOR_EMAIL'),
        packages=['surveys', 'surveys_api'],
        install_requires=[
            'coverage',
            'Django',
            'djangorestframework',
            'drf-extensions',
            'drf-yasg',
            'Faker',
            'factory_boy',
            'psycopg2',
            'python-decouple',
            ],
        scripts=['manage.py']
)

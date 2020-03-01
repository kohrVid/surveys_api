from setuptools import setup, find_packages

setup(
        name= 'surveys_api',
        version='1.0',
        description='An API for studies',
        author='Jessica Été',
        author_email='kohrVid@zoho.com',
        packages=['surveys', 'surveys_api'],
        install_requires=[
            'Django',
            'psycopg2',
            'python-decouple',
            ],
        scripts=['manage.py']
)

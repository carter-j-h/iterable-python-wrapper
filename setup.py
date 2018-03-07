# from distutils.core import setup
from setuptools import setup


long_description = '''
Iterable Python is a Python client that wraps the Iterable Api.
Originally developed by Carter Hickingbotham.  Current version is 0.7
'''

setup(
	name='iterablepythonwrapper',
	packages=['iterablepythonwrapper'],
	url='https://github.com/carter-j-h/iterable-python-wrapper',
	author='Carter Hickingbotham',
	author_email='carterhickingbotham@gmail.com',
	license= 'MIT',
	version='0.7',	
	install_requires=['peppercorn'],
	keywords = ['Iterable', 'API', 'Wrapper', 'Client', 'Python'],
    description='Python Client for the Iterable API',
    long_description=long_description

	)
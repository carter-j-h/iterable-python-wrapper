from distutils.core import setup


long_description = '''
Iterable Python is a Python client that wraps the Iterable Api.
Originally developed by Carter Hickingbotham.
'''

setup(
	name='iterablepythonwrapper',
	packages=['iterablepythonwrapper'],
	url='https://github.com/carter-j-h/iterable-python-wrapper',
	download_url='https://github.com/carter-j-h/iterablepythonwrapper/archive/0.1.tar.gz',
	author='Carter Hickingbotham',
	author_email='carterhickingbotham@gmail.com',
	license= 'MIT',
	version='0.1',	
	install_requires=['peppercorn'],
	keywords = ['Iterable', 'API', 'Wrapper', 'Client', 'Python'],
    description='Python Client for the Iterable Api',
    long_description=long_description

	)
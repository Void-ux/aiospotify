import re
from setuptools import setup

version = ''
with open('spotify/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setup(
    name='aiospotify',
    author='Void-ux',
    url='https://github.com/Void-ux/aio-spotify/',
    version=version,
    packages=['aiospotify'],
    package_data={'aiospotify': ['py.typed']},
    license='MIT',
    description='A simple API wrapper for Spotify.',
    include_package_data=True,
    python_requires='>=3.8.0',
)

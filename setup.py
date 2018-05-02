from setuptools import setup
import re
with open('smartcar/__init__.py','r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)
setup(
    name='smartcar',
    version=version,
    description='Smartcar Python SDK',
    author='Smartcar',
    author_email='hello@smartcar.com',
    packages=['smartcar'],
    url='https://github.com/smartcar/python-sdk',
    license='MIT',
    install_requires=[
        'python-dateutil',
        'requests',
    ],
    extras_require={
        'dev': [
            'coverage',
            'nose',
            'mock',
            'responses',
        ]
    }
)

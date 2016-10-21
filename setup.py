from setuptools import setup
from smartcar import __version__

setup(
    name="smartcar",
    version=__version__,
    description="Smartcar Python SDK",
    author="Zane Bradley",
    author_email="zane@smartcar.com",
    packages=["smartcar"],
    url="https://github.com/smartcar/python-sdk",
    license="MIT",
    install_requires=[
        "requests"
    ]
)
        


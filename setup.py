from setuptools import setup
import re


def _get_version():
    """Extract version from package."""
    with open("smartcar/__init__.py") as reader:
        match = re.search(
            r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', reader.read(), re.MULTILINE
        )
        if match:
            return match.group(1)
        else:
            raise RuntimeError("Unable to extract version.")


def _get_long_description():
    """Get README contents."""
    with open("README.md") as reader:
        return reader.read()


setup(
    name="smartcar",
    version=_get_version(),
    description="Smartcar Python SDK",
    long_description=_get_long_description(),
    long_description_content_type="text/markdown",
    author="Smartcar",
    author_email="hello@smartcar.com",
    packages=["smartcar"],
    url="https://github.com/smartcar/python-sdk",
    license="MIT",
    install_requires=[
        "python-dateutil",
        "requests",
    ],
    extras_require={
        "dev": [
            "black",
            "ipdb",
            "mock",
            "responses",
            "pytest",
            "pytest-cov",
            "selenium",
            "retrying",
            "wheel",
        ]
    },
)

import os
import re

# ===========================================
# Constants
# ===========================================

API_URL = os.environ.get("SMARTCAR_API_ORIGIN", "https://api.smartcar.com")
AUTH_URL = os.environ.get(
    "SMARTCAR_AUTH_ORIGIN", "https://auth.smartcar.com/oauth/token"
)
CONNECT_URL = "https://connect.smartcar.com"
API_VERSION = "2.0"


# ===========================================
# Methods
# ===========================================


def set_api_version(version: str) -> None:
    """
    Update the version of Smartcar API you are using

    Args:
        version (str): the version of the api you want to use
    """
    if re.match(r"\d+\.\d+", version):
        global API_VERSION
        API_VERSION = version
    else:
        raise ValueError(
            fr"Version '{version}' must match regex '\d+\.\d+' .  e.g. '2.0', '1.0'"
        )

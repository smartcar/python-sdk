import os

API_URL = os.environ.get("SMARTCAR_API_ORIGIN", "https://api.smartcar.com")
AUTH_URL = os.environ.get(
    "SMARTCAR_AUTH_ORIGIN", "https://auth.smartcar.com/oauth/token"
)
CONNECT_URL = "https://connect.smartcar.com"

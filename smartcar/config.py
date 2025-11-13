import os

API_ORIGIN = os.environ.get("SMARTCAR_API_ORIGIN", "https://api.smartcar.com")
AUTH_ORIGIN = os.environ.get(
    "SMARTCAR_AUTH_ORIGIN", "https://auth.smartcar.com/oauth/token"
)
CONNECT_ORIGIN = os.environ.get(
    "SMARTCAR_CONNECT_ORIGIN", "https://connect.smartcar.com"
)
MANAGEMENT_API_ORIGIN = os.environ.get(
    "SMARTCAR_MANAGEMENT_API_ORIGIN", "https://management.smartcar.com"
)
VEHICLE_API_ORIGIN = os.environ.get(
    "SMARTCAR_VEHICLE_API_V3_ORIGIN", "https://vehicle.api.smartcar.com"
)

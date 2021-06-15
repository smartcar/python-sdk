__version__ = "semantic-release"

from smartcar.auth_client import AuthClient

from smartcar.static import (
    set_api_version,
    get_user,
    get_vehicles,
    get_compatibility
)

from smartcar.vehicle import Vehicle

from smartcar.exceptions import (
    SmartcarException,
    SmartcarExceptionV2,
    ValidationException,
    AuthenticationException,
    PermissionException,
    ResourceNotFoundException,
    StateException,
    RateLimitingException,
    MonthlyLimitExceeded,
    ServerException,
    VehicleNotCapableException,
    SmartcarNotCapableException,
    GatewayTimeoutException,
)

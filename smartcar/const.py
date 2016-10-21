import json
API_VERSION = "1.0"
API_URL = "https://api.smartcar.com/v{}/vehicles".format(API_VERSION)
AUTH_URL = "https://auth.smartcar.com/oauth/token"
OEMS = {
    "acura": "https://acura.smartcar.com",
    "audi": "https://audi.smartcar.com",
    "fiat": "https://fiat.smartcar.com",
    "ford": "https://ford.smartcar.com",
    "landrover": "https://landrover.smartcar.com",
    "mercedes": "https://mercedes.smartcar.com",
    "tesla": "https://tesla.smartcar.com",
    "volkswagen": "https://volkswagen.smartcar.com",
    "volvo": "https://volvo.smartcar.com",
    "hyundai": "https://hyundai.smartcar.com"
}

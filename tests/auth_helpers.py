import os
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from distutils.util import strtobool

try:
    import urlparse
except BaseException:
    # python 3
    import urllib.parse as urlparse

if (
    not "E2E_SMARTCAR_CLIENT_ID" in os.environ
    or not "E2E_SMARTCAR_CLIENT_SECRET" in os.environ
):
    raise Exception(
        '"E2E_SMARTCAR_CLIENT_ID" and "E2E_SMARTCAR_CLIENT_SECRET" environment variables must be set'
    )

HEADLESS = "CI" in os.environ or (
    "HEADLESS" in os.environ and strtobool(os.environ["HEADLESS"])
)
CLIENT_ID = os.environ["E2E_SMARTCAR_CLIENT_ID"]
CLIENT_SECRET = os.environ["E2E_SMARTCAR_CLIENT_SECRET"]
REDIRECT_URI = "https://example.com/auth"

DEFAULT_SCOPE = [
    "required:read_vehicle_info",
    "required:read_location",
    "required:read_odometer",
    "required:control_security",
    "required:read_vin",
    "required:read_fuel",
    "required:read_battery",
    "required:read_charge",
    "required:read_engine_oil",
    "required:read_tires",
]


def get_auth_client_params():
    test_mode = True
    return [CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, test_mode]


def get_code_from_url(url):
    search_params = urlparse.parse_qs(urlparse.urlparse(url).query)

    if "code" not in search_params:
        raise Exception(
            "Did not get code in url! Query string: {}".format(search_params["error"])
        )

    return search_params["code"]


def run_auth_flow(auth_url, brand="CHEVROLET"):
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = HEADLESS
    driver = webdriver.Firefox(options=firefox_options)

    driver.get(auth_url)

    # Preamble
    preamble_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button#continue-button"))
    )
    preamble_button.click()

    # Brand Selector
    brand_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "button.brand-selector-button[data-make='{}']".format(brand),
            )
        )
    )
    brand_button.click()

    username = str(uuid.uuid4()) + "@email.com"
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sign-in-button"))
    )
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys("password")
    sign_in_button.click()

    permissions_approval_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "approval-button"))
    )
    permissions_approval_button.click()
    url = driver.current_url
    driver.close()
    return get_code_from_url(url)

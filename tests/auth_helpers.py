import os
import uuid
import urllib.parse as urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from distutils.util import strtobool

import smartcar.helpers as helpers

# Verify all E2E variables are present ('E2E_<CLIENT VARIABLE>')
helpers.validate_env(mode="test")

# Smartcar client environment variables (Required)
CLIENT_ID = os.environ["E2E_SMARTCAR_CLIENT_ID"]
CLIENT_SECRET = os.environ["E2E_SMARTCAR_CLIENT_SECRET"]
REDIRECT_URI = "https://example.com/auth"

# Variables for testing webhooks (Optional):
APPLICATION_MANAGEMENT_TOKEN = os.environ.get("E2E_SMARTCAR_AMT")
WEBHOOK_ID = os.environ.get("E2E_SMARTCAR_WEBHOOK_ID")

# Variables for Geckodriver
HEADLESS = "CI" in os.environ or (
    "HEADLESS" in os.environ and strtobool(os.environ["HEADLESS"])
)

# A list of all available permissions on Smartcar API
DEFAULT_SCOPE = [
    "required:read_vehicle_info",
    "required:read_location",
    "required:read_odometer",
    "required:control_security",
    "required:read_vin",
    "required:read_fuel",
    "required:read_battery",
    "read_charge",
    "required:read_engine_oil",
    "required:read_tires",
]


def get_auth_client_params():
    mode = "test"
    return [CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, True, mode]


def get_code_from_url(url):
    search_params = urlparse.parse_qs(urlparse.urlparse(url).query)

    if "code" not in search_params:
        raise Exception(
            f"Did not get code in url! Query string: {search_params['error']}"
        )

    return search_params["code"]


def run_auth_flow(auth_url, brand="CHEVROLET"):
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = HEADLESS
    driver = webdriver.Firefox(options=firefox_options)

    driver.get(auth_url)
    # Preamble
    preamble_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button#continue-button"))
    )
    preamble_button.click()

    # Brand Selector
    brand_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"button#{brand.upper()}.brand-list-item")
        )
    )
    brand_button.click()

    # Logging in (with any random credentials to run through test-mode)
    username = str(uuid.uuid4()) + "@email.com"
    sign_in_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "sign-in-button"))
    )
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys("password")
    sign_in_button.click()

    # Permissions Approval
    permissions_approval_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "approval-button"))
    )
    permissions_approval_button.click()
    WebDriverWait(driver, 30).until(EC.url_matches("example.com"))

    # Capture URL and get the access `code`
    url = driver.current_url
    driver.close()
    return get_code_from_url(url)

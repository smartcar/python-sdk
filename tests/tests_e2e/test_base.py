from retrying import retry
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import uuid
try:
    import urlparse
except BaseException:
    # python 3
    import urllib.parse as urlparse

import smartcar


class TestBase(unittest.TestCase):

    @classmethod
    @retry
    def setUpClass(cls):
        def get_code(driver, auth_url):
            driver.get(auth_url)

            mock_smartcar_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "/html/body/div/a[starts-with(@href, 'https://mock.smartcar.com')]")))
            mock_smartcar_button.click()

            username = uuid.uuid4()
            username = str(username) + '@mock.com'

            approval_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'approval-button')))
            driver.find_element_by_id('username').send_keys(username)
            driver.find_element_by_id('password').send_keys('password')
            approval_button.click()

            permissions_approval_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'approval-button')))
            permissions_approval_button.click()

            url = driver.current_url
            parsed_url = urlparse.urlparse(url)
            return urlparse.parse_qs(parsed_url.query)['code'][0]

        client_id = os.environ['INTEGRATION_CLIENT_ID']
        client_secret = os.environ['INTEGRATION_CLIENT_SECRET']
        redirect_uri = 'https://example.com/auth'
        scope = [
            'control_security:unlock',
            'control_security:lock',
            'read_vehicle_info',
            'read_vin',
            'read_location',
            'read_odometer'
        ]
        test_mode = True

        cls.client = smartcar.AuthClient(
            client_id,
            client_secret,
            redirect_uri,
            scope,
            test_mode
        )

        cls.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
            keep_alive=True)

        auth_url = cls.client.get_auth_url()

        cls.code = get_code(cls.driver, auth_url)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

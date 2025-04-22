import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from fusionpbx_pilot.page_objects import FusionPBX

load_dotenv()

try:
    service = FirefoxService()
except ValueError as e:
    print(f"Error: {e}")
    service = FirefoxService(GeckoDriverManager().install())
    

url = os.getenv("PYTEST_URL")
username = os.getenv("PYTEST_USERNAME")
password = os.getenv("PYTEST_PASSWORD")

@pytest.fixture
def fusionpbx():
    """Fixture to create a FusionPBX instance for each test."""
    with FusionPBX(webdriver.Firefox(service=service), url, username, password) as fusionpbx:
        yield fusionpbx

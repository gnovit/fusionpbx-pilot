import os

import pytest
from dotenv import load_dotenv
from faker import Faker
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from fusionpbx_pilot.page_objects import FusionPBX

load_dotenv()

try:
    service = FirefoxService()
except ValueError as e:
    print(f'Error: {e}')
    service = FirefoxService(GeckoDriverManager().install())

fake = Faker()
fake_domain = fake.domain_name()


@pytest.fixture
def test_domain():
    """Fixture to provide a fake domain name."""
    return fake_domain


@pytest.fixture
def fusionpbx():
    """Fixture to create a FusionPBX instance for each test."""
    with FusionPBX(
        webdriver.Firefox(service=service),
        os.getenv('PYTEST_URL'),
        os.getenv('PYTEST_USERNAME'),
        os.getenv('PYTEST_PASSWORD'),
    ) as fusionpbx:
        yield fusionpbx


# @pytest.fixture
# def domain_created(fusionpbx):
#     """Fixture to create a domain."""
#     d = fusionpbx.domain(fake.domain_name(), create=True)
#     return d.name

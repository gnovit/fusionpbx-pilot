import os

from dotenv import load_dotenv
from faker import Faker
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.fiquirefox import GeckoDriverManager

from fusionpbx_pilot.page_objects import FusionPBX

load_dotenv(dotenv_path='/home/marcelo/dev/fusionpbx-pilot/samples/.env')

try:
    service = FirefoxService()
except ValueError as e:
    print(f'Error: {e}')
    service = FirefoxService(GeckoDriverManager().install())

fake = Faker()
fake_domain = fake.domain_name()

f = FusionPBX(
    webdriver.Firefox(service=service),
    os.getenv('PYTEST_URL'),
    os.getenv('PYTEST_USERNAME'),
    os.getenv('PYTEST_PASSWORD'),
)

d = f.domain(fake_domain)



from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

browser = Firefox()
wdw = WebDriverWait(browser, 10)
url = "https://45.79.223.247"
user = "admin"
password = "S3nh4C0mpl3x4$"


class FindByLocator(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, webdriver):
        element = webdriver.find_elements(*self.locator)
        if element:
            return element
        return False


class MainMenu(object):

    def __init__(self, wdw):
        self.wdw = wdw
        self._menu = self.wdw.until(FindByLocator((By.XPATH, "//div[@id='main_navbar']/ul[@class='navbar-nav']")))
        self._menu_items = self._menu[0].find_elements((By.TAG_NAME, 'li'))

    def click(self, menu_item: dict):
        # click on menu item
        pass


def fill_form(locator: tuple, text: str, WebDriverWait):
    field = WebDriverWait.until(FindByLocator(locator))
    field[0].send_keys(text)


browser.get(url)

# login
fill_form((By.ID, "username"), user, wdw)
fill_form((By.NAME, "password"), password, wdw)
wdw.until(FindByLocator((By.ID, "btn_login")))[0].click()

main_menu = MainMenu(wdw)

pass

# Create Domain
domain = 'capivara.com'
url = "https://45.79.223.247/core/domains/domains.php"
browser.get(url)
wdw.until(FindByLocator((By.ID, "btn_add")))[0].click()
fill_form((By.NAME, "domain_name"), domain, wdw)
wdw.until(FindByLocator((By.ID, "btn_save")))[0].click()
domains = wdw.until(FindByLocator((By.CLASS_NAME, 'list-row')))

main_menu = wdw.until(FindByLocator((By.XPATH, "//div[@id='main_navbar']/ul[@class='navbar-nav']")))

pass

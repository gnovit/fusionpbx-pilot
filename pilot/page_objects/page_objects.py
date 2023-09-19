from abc import ABC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class LoginError(Exception):
    def __init__(self, message=None):
        if message is None:
            message = "Login error"
        super().__init__(message)


class AccessError(Exception):
    def __init__(self, message=None):
        if message is None:
            message = "No permission error"
        super().__init__(message)


class SelectError(Exception):
    def __init__(self, message=None):
        if message is None:
            message = "Select error"
        super().__init__(message)


class SeleniumObject(ABC):
    """Base class to handle selenium objects"""

    def find_element(self, locator: tuple):
        return self.webdriver.find_element(*locator)

    def find_elements(self, locator: tuple):
        return self.webdriver.find_elements(*locator)

    def fill_form(self, locator: tuple, text: str, clear=True):
        field = self.find_element(locator)
        if clear:
            field.clear()
        field.send_keys(text)

    def click_button(self, locator: tuple):
        self.find_element(locator).click()

    def _open(self, url: str):
        return self.webdriver.get(url)


class Page(SeleniumObject, ABC):
    """Base class to handle page elements"""

    def __init__(self, webdriver, base_url, login_user, login_password):
        self.webdriver = webdriver
        self.base_url = base_url
        self.login_user = login_user
        self.login_password = login_password

    def container_rows(self, items: dict[str:tuple] = None) -> list[dict]:
        """Return a dict with the item:uuid rows
        Default items are name: uuid

        Args:
            items (dict[str:tuple], optional): Dict of locator tuples to return where key is the name of attr. Defaults to None.

        Returns:
            dic: {name: uuid, item[key]: value}
        """
        container_rows = self.find_elements((By.CLASS_NAME, "list-row"))
        cr = []
        for row in container_rows:
            d = {}
            uuid = row.find_element(
                By.CSS_SELECTOR, "input[type='hidden']"
            ).get_attribute("value")
            name = row.find_element(By.CSS_SELECTOR, "td a[title='Edit']").text
            d[name] = uuid
            if items:
                for key in items:
                    key_value = row.find_element(*items[key]).text
                    d[key] = key_value
            cr.append(d)
        return cr

    def select_rows(self, names: list[str]):
        """Select rows by name of objects

        Args:
            names (list[str]): List of name to select
        """
        if not isinstance(names, list):
            raise TypeError("names must be a list")

        container_rows = self.container_rows()
        for name in names:
            for row in container_rows:
                if name in row:
                    hidden_element = self.find_element(
                        (By.CSS_SELECTOR, f"input[value='{row[name]}']")
                    )
                    hidden_element.find_element(By.XPATH, "..").click()
                else:
                    raise SelectError(f"Name {name} not found in rows")

    def has_permission(self):
        """Check if the current user has permission to access the page

        Returns:
            bool: True if has permission
        """
        if self.find_element((By.TAG_NAME, "body")).text == "access denied":
            return False
        else:
            return True

    def open(self, url):
        self._open(self.base_url + url)
        # TODO: Maybe check cookie?
        if "login.php" in self.webdriver.current_url or "Login" in self.webdriver.title:
            self.login(self.login_user, self.login_password)
        if self.webdriver.current_url != self.base_url + url:
            self._open(self.base_url + url)
        if self.has_permission():
            return
        else:
            raise AccessError(
                f"User {self.login_user} has no permission to access page {self.base_url + url}"
            )
        return

    def login(self, login_user, login_password):
        self.fill_form((By.ID, "username"), login_user)
        self.fill_form((By.NAME, "password"), login_password)
        self.click_button((By.ID, "btn_login"))
        if "login.php" in self.webdriver.current_url:
            raise LoginError(
                f"Login failed for {self.login_user}, password: {self.login_password}"
            )
        return

    def get_bool_from_list_field(self, locator: tuple):
        field = self.find_element(locator)
        dropdown = Select(field)
        if dropdown.first_selected_option.accessible_name == "True":
            return True
        elif dropdown.first_selected_option.accessible_name == "False":
            return False

    def set_bool_from_list_field(self, locator: tuple, value: bool):
        if not isinstance(value, bool):
            raise TypeError("value must be boolean")

        field = self.find_element(locator)
        dropdown = Select(field)
        if value:
            dropdown.select_by_value("true")
            return value
        elif not value:
            dropdown.select_by_value("false")
            return value

    def search_field(self, text: str):
        self.fill_form((By.ID, "search"), text)
        self.click_button((By.ID, "btn_search"))
        return self.container_rows_to_dict()

from abc import ABC
from pilot.page_objects.apps import Extension
from pilot.page_objects.apps import Extensions
from selenium.webdriver.common.by import By
from pilot.page_objects.page_objects import AccessError
from selenium.common.exceptions import NoSuchElementException



app_path = "/core/domains/domains.php"
app_edit_path = "/core/domains/domain_edit.php"


class DomainNotFound(Exception):
    def __init__(self, domain_name, message=None):
        if message is None:
            message = f"Extension {domain_name} not found"
        super().__init__(message)
        self.domain_name = domain_name


class Domain(ABC):
    """FusionPBX class to handle domain management and apps related."""

    def __init__(self, page):
        self.page = page
        self.uuid = None

    def __call__(self, name):
        self.name = name
        return self

    @property
    def extensions(self):
        return Extensions(self.page)

    @property
    def extension(self):
        return Extension(self.page)

    @extension.setter
    def extension(self, name):
        self.extension.name = name

    @extension.deleter
    def extension(self, name):
        self.extension.name = name
        del self.extension.name

    def _switch_to(self, name):
        self.page.open(f"{app_path}?domain_uuid={self.uuid}&domain_change=true")

    @property
    def name(self):
        """Return the current domain"""
        try:
            self.page.open(app_path)
            try:
                return self.page.find_element(
                    (By.XPATH, "//*[@id='header_domain_selector_domain']")
                ).text
            except NoSuchElementException:
                # Fusionpbx Version  4.5.28 
                return self.page.find_element((By.CSS_SELECTOR, ".domain_selector_domain")).text

        except AccessError:
            return self.page.login_user.split("@")[1]

    @name.setter
    def name(self, name: str):
        """Set/Rename the current domain name"""
        self.page.open(app_path)
        search = self.page.search_exact_name(name)
        if self.uuid is None:
            if search and search['name'] == name:
                # Already exists
                self.uuid = search['uuid']
                self._switch_to(name)
                return self.name
            else:
                # Create
                self.page.open(app_path)
                self.page.click_button((By.ID, "btn_add"))
                self.page.fill_form((By.NAME, "domain_name"), name)
                self.page.click_button((By.ID, "btn_save"))
                self.page.open(app_path)
                self.uuid = self.page.search_exact_name(name)['uuid']
                return self._switch_to(name)
        elif self.uuid is not None:
            # Rename
            if name in search:
                raise Exception(f"Domain {name} already exists")
            self.page.open(f"{app_edit_path}?id={self.uuid}")
            self.page.fill_form((By.NAME, "domain_name"), name)
            return self._switch_to(name)

    @name.deleter
    def name(self):
        """Delete the current domain"""
        self.page.open(app_path)
        self.page.click_button(
            (By.XPATH, f"//a[text()='{self.name}']/../..//input[@type='checkbox']")
        )
        self.page.click_button((By.ID, "btn_delete"))
        #
        self.page.click_button(
            (By.XPATH, '//button[@id="btn_delete"][@title="Continue"]')
        )
        # self._list = self.list

    def __repr__(self):
        return f"<Domain: {self.name}>"

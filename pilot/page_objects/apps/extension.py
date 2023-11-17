from abc import ABC
from selenium.webdriver.common.by import By

app_path = "/app/extensions/extensions.php"
app_edit_path = "/app/extensions/extension_edit.php"


class ExtensionNotFound(Exception):
    def __init__(self, extension_name, message=None):
        if message is None:
            message = f"Extension {extension_name} not found"
        super().__init__(message)
        self.extension_name = extension_name


class Extension(ABC):
    """FusionPBX class to handle extension management"""

    def __init__(self, page):
        self.page = page
        self.uuid = None

    def __call__(self, name):
        self.name = name
        return self

    def _satity_check(self):
        if not self.uuid:
            raise ExtensionNotFound(None)

    @property
    def name(self):
        if hasattr(self, "_name"):
            return self._name
        else:
            return None

    @name.setter
    def name(self, name: str):
        """Set/Rename the current extension name"""
        self.page.open(app_path)
        search = self.page.search_exact_name(name)
        if self.uuid is None:
            if search and search['name']:
                # Already exists
                self.uuid = search['uuid']
                self._name = str(name)
                return self.name
            else:
                # Create
                self.page.open(app_path)
                self.page.click_button((By.ID, "btn_add"))
                self.page.fill_form((By.NAME, "extension"), name)
                self.page.click_button((By.ID, "btn_save"))
                self._name = str(name)
                self.page.open(app_path)
                self.uuid = self.page.search_exact_name(name)['uuid']
                return self.name

        elif self.uuid is not None:
            # Rename
            if name in search:
                raise Exception(f"Extension {name} already exists")

            self.page.open(f"{app_edit_path}?id={self.uuid}")
            self.page.fill_form((By.NAME, "extension"), name)
            self.page.click_button((By.ID, "btn_save"))
            self._name = str(name)
            # self._list = self.list
            return self.name

    @name.deleter
    def name(self):
        """Delete the current extension"""
        self.page.open(app_path)
        self.page.click_button(
            (By.XPATH, f"//a[text()='{self._name}']/../..//input[@type='checkbox']")
        )
        self.page.click_button((By.ID, "btn_delete"))
        self.page.click_button((By.XPATH, "//span[text()='Extension & Voicemail']"))
        del self._name

    @property
    def password(self):
        self._satity_check()
        self.page.open(f"{app_edit_path}?id={self.uuid}")
        return self.page.find_element((By.ID, "password")).get_attribute("value")

    @password.setter
    def password(self, password):
        """Set the current password"""
        self._satity_check()
        self.page.open(f"{app_edit_path}?id={self.uuid}")
        self.page.fill_form((By.NAME, "password"), password)
        self.page.click_button((By.ID, "btn_save"))
        return self.password

    @property
    def voicemail_mail_to(self):
        self._satity_check()
        self.page.open(f"{app_edit_path}?id={self.uuid}")
        return self.page.find_element((By.NAME, "voicemail_mail_to")).get_attribute("value")

    @voicemail_mail_to.setter
    def voicemail_mail_to(self, email):
        """Set the current voicemail_mail_to"""
        self._satity_check()
        self.page.open(f"{app_edit_path}?id={self.uuid}")
        self.page.fill_form((By.NAME, "voicemail_mail_to"), email)
        self.page.click_button((By.ID, "btn_save"))
        return self.voicemail_mail_to

    @voicemail_mail_to.deleter
    def voicemail_mail_to(self):
        """Delete the current voicemail_mail_to"""
        self._satity_check()
        self.page.open(f"{app_edit_path}?id={self.uuid}")
        locator = (By.NAME, "voicemail_mail_to")
        field = self.page.find_element(locator)
        field.clear()
        self.page.click_button((By.ID, "btn_save"))
        return self.voicemail_mail_to

    @property
    def voicemail_enabled(self):
        self._satity_check()
        self.page.open(f"{app_edit_path}?id={self.uuid}")
        value = self.page.get_bool_from_list_field((By.NAME, "voicemail_enabled"))
        return value

    @voicemail_enabled.setter
    def voicemail_enabled(self, enabled: bool):
        """Set the current voicemail_enabled"""
        self._satity_check()
        if enabled != self.voicemail_enabled:
            self.page.open(f"{app_edit_path}?id={self.uuid}")
            self.page.set_bool_from_list_field((By.NAME, "voicemail_enabled"), enabled)
            self.page.click_button((By.ID, "btn_save"))
        return self.voicemail_enabled

    def __repr__(self):
        return f"<Extension: {self.name}>"

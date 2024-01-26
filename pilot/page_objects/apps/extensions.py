from abc import ABC
from selenium.webdriver.common.by import By

app_path = "/app/extensions/extensions.php"
app_edit_path = "/app/extensions/extension_edit.php"


class ExtensionNotFound(Exception):
    """Exception raised when an extension is not found."""

    def __init__(self, extension_name, message=None):
        if message is None:
            message = f"Extension {extension_name} not found"
        super().__init__(message)
        self.extension_name = extension_name


class Extensions(ABC):
    """FusionPBX class to handle extension management"""

    def __init__(self, page):
        self.page = page
        self.uuid = None

    class Extensions:
        def list(self):
            """
            Retrieves a list of extensions from the page.

            Returns:
                dict: A dictionary containing the enabled status and description of each extension.
            """
            self.page.open(app_path)
            items = {
                "enabled": (By.CSS_SELECTOR, 'td button[title="Toggle"] span'),
                "description": (
                    By.CSS_SELECTOR,
                    'td[class="description overflow hide-sm-dn"]',
                ),
            }
            return self.page.container_rows(items)

    def toggle(self, extensions: list):
        """Toggle extensions Enabled/Disabled

        Args:
            extensions (list): List of extensions to toggle

        Returns:
            None
        """

        self.page.open(app_path)
        self.page.select_rows(extensions)
        # WIP: Need to click on toogle button to complete the action

    def __repr__(self):
        return f"<Extension: {self.list}>"

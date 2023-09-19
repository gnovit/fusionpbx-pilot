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

    @property
    def list(self):
        self.page.open(app_path)
        return self.page.container_rows_to_dict()
    
    def toggle(self, list[extension]):
        pass

    def 

    def __repr__(self):
        return f"<Extension: {self.list}>"

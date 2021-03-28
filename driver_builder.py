from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import settings


class DriverBuilder:
    @staticmethod
    def build():
        chrome_options = Options()
        chrome_options.add_extension('./recruiters_integration_tool.crx')
        return webdriver.Chrome(executable_path=settings.CHROME_DRIVER_PATH,
                                chrome_options=chrome_options)

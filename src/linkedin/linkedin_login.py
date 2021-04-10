import settings
import time


class LinkedinLogin:
    def __init__(self, driver):
        self.driver = driver

    def login(self):
        self.driver.get(settings.LINKEDIN_URL)

        email_field = self.driver.find_element_by_id('session_key')
        email_field.send_keys(settings.LINKEDIN_EMAIL)
        # time.sleep(0.5)

        password_field = self.driver.find_element_by_id('session_password')
        password_field.send_keys(settings.LINKEDIN_PASSWORD)
        # time.sleep(0.5)

        sign_in_button = self.driver.find_element_by_xpath('//*[@type="submit"]')
        sign_in_button.click()

from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
import settings


class CleverstaffLogin:
    def __init__(self, driver):
        self.driver = driver

    def login(self):
        self.driver.get(settings.CLEVERSTAFF_URL)

        email_field = self.driver.find_element_by_id('user-email')
        email_field.send_keys(settings.ATS_EMAIL)

        password_field = self.driver.find_element_by_id('login-password')
        password_field.send_keys(settings.ATS_PASSWORD)

        try:
            cookies_button = self.driver.find_element_by_id('cookie-agree-btn')
            cookies_button.click()
        except (ElementNotInteractableException, NoSuchElementException):
            pass

        sign_in_button = self.driver.find_element_by_xpath('//*[@type="submit"]')
        sign_in_button.click()

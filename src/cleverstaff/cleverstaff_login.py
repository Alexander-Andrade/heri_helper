import settings


class CleverstaffLogin:
    def __init__(self, driver):
        self.driver = driver

    def login(self):
        self.driver.get(settings.CLEVERSTAFF_URL)

        email_field = self.driver.find_element_by_id('user-email')
        email_field.send_keys(settings.ATS_EMAIL)
        # time.sleep(0.5)

        password_field = self.driver.find_element_by_id('login-password')
        password_field.send_keys(settings.ATS_PASSWORD)
        # time.sleep(0.5)

        sign_in_button = self.driver.find_element_by_xpath('//*[@type="submit"]')
        sign_in_button.click()

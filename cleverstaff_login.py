import settings
from cookies_processor import CookiesProcessor


class CleverstaffLogin:
    CLEVERSTAFF_URL = 'https://cleverstaff.net/ru/signin.html'
    COOKIE_FILENAME = 'cleverstaff_cookie.pkl'

    def __init__(self, driver, load_cookies=False, store_cookies=False):
        self.driver = driver
        self.load_cookies = load_cookies
        self.store_cookies = store_cookies

    def login(self):
        self.driver.get(self.CLEVERSTAFF_URL)

        if self.load_cookies:
            CookiesProcessor(
                driver=self.driver,
                filename=self.COOKIE_FILENAME
            ).load()
        else:
            email_field = self.driver.find_element_by_id('user-email')
            email_field.send_keys(settings.ATS_EMAIL)
            # time.sleep(0.5)

            password_field = self.driver.find_element_by_id('login-password')
            password_field.send_keys(settings.ATS_PASSWORD)
            # time.sleep(0.5)

            sign_in_button = self.driver.find_element_by_xpath('//*[@type="submit"]')
            sign_in_button.click()

        if self.store_cookies:
            CookiesProcessor(
                driver=self.driver,
                filename=self.COOKIE_FILENAME
            ).store()

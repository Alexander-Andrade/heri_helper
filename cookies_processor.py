import pickle


class CookiesProcessor:
    def __init__(self, driver, filename):
        self.driver = driver
        self.filename = filename

    def store(self):
        pickle.dump(self.driver.get_cookies(), open(self.filename, "wb"))

    def load(self):
        cookies = pickle.load(open(self.filename, "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)

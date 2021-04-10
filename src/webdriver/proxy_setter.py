from selenium import webdriver


class ProxySetter:
    @staticmethod
    def set(proxy):
        if proxy:
            webdriver.DesiredCapabilities.CHROME['proxy'] = {
                "httpProxy": proxy,
                "ftpProxy": proxy,
                "sslProxy": proxy,
                "proxyType": "MANUAL",

            }
            return True
        return False

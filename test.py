from src.linkedin.linkedin_login import LinkedinLogin
from src.linkedin.linkedin_search import LinkedinSearch
from src.webdriver.driver_builder import DriverBuilder

if __name__ == '__main__':
    driver = DriverBuilder.build()
    LinkedinLogin(driver=driver).login()
    res = search_result = LinkedinSearch(
        driver=driver,
        query='python developer minsk',
        pages=['1', '14']
    ).search()
    if res.is_failure():
        print(res.error)
    else:
        print(res.data)

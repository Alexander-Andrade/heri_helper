from selenium.webdriver.common.keys import Keys
import selenium
import settings
from result import Result


class LinkedinGoogleSearch:
    GOOGLE_URL = 'https://www.google.com'

    def __init__(self, driver, query, pages):
        self.query = query
        self.driver = driver
        self.pages = sorted(pages)

    def search(self):
        self.driver.get(self.GOOGLE_URL)
        search_query = self.driver.find_element_by_name('q')
        search_query.send_keys(self.query)
        search_query.send_keys(Keys.RETURN)

        linkedin_urls = []
        for page in self.pages:
            navigation_result = self.go_to_page(page)
            if navigation_result.is_failure():
                return navigation_result

            linkedin_urls = linkedin_urls + self.find_linkedin_urls()
        return Result.success(linkedin_urls)

    def go_to_page(self, page):
        previous_last_visible_page = None
        while True:
            try:
                pagination_button = self.driver.find_element_by_link_text(str(page))
                pagination_button.click()
                return Result.success()
            except selenium.common.exceptions.NoSuchElementException:
                pass

            last_visible_page = self.click_last_visible_page()
            if previous_last_visible_page and last_visible_page <= previous_last_visible_page:
                return Result.failure(f"Searchable page is out of range, last page:"
                                      f" {previous_last_visible_page}, searchable page: #{page}")
            previous_last_visible_page = last_visible_page
            if settings.MAX_PAGE <= last_visible_page:
                return Result.failure(f"MAX_PAGE reached")

    def click_last_visible_page(self):
        last_visible_page_button = self.driver.find_elements_by_class_name('fl')[-1]
        last_visible_page = int(last_visible_page_button.text)
        last_visible_page_button.click()
        return last_visible_page

    def find_linkedin_urls(self):
        link_tags = self.driver.find_elements_by_tag_name('a')

        linkedin_urls = []
        for tag in link_tags:
            href = tag.get_attribute("href")
            if href and 'linkedin.com/in' in href and 'google.com' not in href:
                linkedin_urls.append(href)
        return linkedin_urls

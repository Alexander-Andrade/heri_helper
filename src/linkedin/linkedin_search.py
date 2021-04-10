from selenium.webdriver.common.keys import Keys
import selenium
import settings
from src.result import Result
from selenium.common.exceptions import NoSuchElementException
import time
from .linkedin_paginator import LinkedinPaginator
from ..retry_decorator import retry_if_return_value, retry_if_exception


class LinkedinSearch:
    def __init__(self, driver, query, pages):
        self.query = query
        self.driver = driver
        self.pages = sorted(map(int, pages))

    def search(self):
        self.driver.get(settings.LINKEDIN_URL)
        self.enter_query()

        linkedin_urls = []
        for page in self.pages:
            navigated = LinkedinPaginator(driver=self.driver,
                                          page=page).go_to_page()
            if not navigated:
                return Result.failure(f'Pagination error: page {page}')

            linkedin_urls = linkedin_urls + self.find_linkedin_urls()
        return Result.success(linkedin_urls)

    def enter_query(self):
        time.sleep(1)
        try:
            open_query_button = self.driver. \
                find_element_by_css_selector('button.search-global-typeahead__collapsed-search-button')
            open_query_button.click()
        except NoSuchElementException:
            pass
        time.sleep(1)
        search_query = self.driver. \
            find_element_by_css_selector('input.search-global-typeahead__input')
        search_query.send_keys(self.query)
        search_query.send_keys(Keys.RETURN)

    @retry_if_return_value([])
    def find_linkedin_urls(self):
        links_wrappers = self.driver.find_elements_by_css_selector('span.entity-result__title-text')

        linkedin_urls = []
        for link_wrapper in links_wrappers:
            href = link_wrapper.find_element_by_tag_name('a').get_attribute("href")
            if href and 'linkedin.com/in' in href:
                linkedin_urls.append(href)
        return linkedin_urls

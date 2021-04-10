import time
from ..retry_decorator import retry_if_return_value, retry_if_exception
from selenium.common.exceptions import NoSuchElementException


class LinkedinPaginator:
    def __init__(self, driver, page):
        self.driver = driver
        self.page = page

    def go_to_page(self):
        if self.page == 1:
            self.click_browse_all_button()
            return True

        while True:
            pagination_buttons = self.find_pagination_buttons()
            if not pagination_buttons:
                return False

            if self.try_navigate_to_page(pagination_buttons):
                return True

            if not self.to_next_page_list(pagination_buttons):
                return False

    @retry_if_exception(NoSuchElementException)
    def click_browse_all_button(self):
        browse_all_people_button = self.driver.find_element_by_css_selector(
            'div.search-results__cluster-bottom-banner.artdeco-button.'
            'artdeco-button--tertiary.artdeco-button--muted'
        ).find_element_by_xpath('./a')
        browse_all_people_button.click()

    @retry_if_return_value([])
    def find_pagination_buttons(self):
        pagination_items = self.driver.\
            find_elements_by_css_selector('li.artdeco-pagination__indicator')
        return [li.find_element_by_tag_name('button') for li in pagination_items]

    def try_navigate_to_page(self, pagination_buttons):
        for button in pagination_buttons:
            if button.find_element_by_tag_name('span').text == str(self.page):
                button.click()
                return True
        return False

    def to_next_page_list(self, pagination_buttons):
        for button in reversed(pagination_buttons):
            if button.find_element_by_tag_name('span').text == '…':
                button.click()
                return True
        return False


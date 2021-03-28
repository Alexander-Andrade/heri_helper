from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from result import Result
import time


class AddCandidateToDatabase:
    def __init__(self, driver, candidate_url, vacancy):
        self.driver = driver
        self.vacancy = vacancy
        self.candidate_url = candidate_url

    def add(self):
        time.sleep(3)
        self.driver.get(self.candidate_url)
        time.sleep(0.5)

        try:
            self.driver.find_element_by_css_selector(
                'a.save-button.sign-in-to-ats.LinkedinResume'
            )
            return Result.failure('Sign in to ATS first')
        except NoSuchElementException:
            pass

        try:
            save_to_ats_button = self.driver. \
                find_element_by_css_selector('a.save-button.user-auth.LinkedinResume')
            save_to_ats_button.click()
            time.sleep(10)
        except NoSuchElementException:
            return Result.failure(
                f'Save to ATS button was not present for {self.candidate_url}'
            )

        dropdown_input = self.driver.find_element_by_css_selector('input.vacancy-dropdown__input')
        dropdown_input.click()

        vacancy_option_result = self.find_vacancy_option()
        if vacancy_option_result.is_failure():
            return vacancy_option_result

        vacancy_option_result.data.click()
        save_to_ats_button = self.driver.\
            find_element_by_xpath("//button[contains(text(), 'ATS')]")
        save_to_ats_button.click()

        return Result.success(f'{self.candidate_url} added to ATS database')

    def find_vacancy_option(self):
        vacancies_options = self.driver.find_elements_by_css_selector(
            "span.vacancy-dropdown__autocomplete-option-text"
        )
        lower_vacancy = self.vacancy.lower()
        for option in vacancies_options:
            if lower_vacancy in option.text.lower():
                return Result.success(option)
        return Result.failure(f'Can not find \'{self.vacancy}\' in ATS options')

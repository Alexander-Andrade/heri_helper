from selenium.common.exceptions import NoSuchElementException
from src.result import Result
from urllib.parse import unquote
from src.retry_decorator import retry_if_exception
import time


class AddCandidateToDatabase:
    def __init__(self, driver, candidate_url, vacancy):
        self.driver = driver
        self.vacancy = vacancy
        self.candidate_url = candidate_url

    def add(self):
        time.sleep(1)
        self.driver.get(self.candidate_url)
        time.sleep(3)

        signedin_to_ats = self.check_signed_in_to_ats()
        if not signedin_to_ats:
            return Result.failure('Sign in to ATS first')

        profile_in_ats = self.check_profile_in_ats()
        if profile_in_ats:
            return Result.success(f'Profile in ATS {unquote(self.candidate_url)}')

        save_to_ats_pressed = self.press_save_to_ats_button()
        if not save_to_ats_pressed:
            return Result.failure(f'Save to ATS button was'
                                  f' not present for {unquote(self.candidate_url)}')

        self.try_save_to_new_vacancy()

        vacancy_selected = self.select_vacancy()
        if not vacancy_selected:
            Result.failure(f'Can not find \'{self.vacancy}\' in ATS options')

        self.press_add_to_vacancy_in_ats()

        return Result.success(f'{unquote(self.candidate_url)} added to ATS database')

    @retry_if_exception(NoSuchElementException)
    def press_add_to_vacancy_in_ats(self):
        add_to_vacancy_in_ats_button = self.driver.\
            find_element_by_xpath("//button[contains(text(), 'Add to vacancy in ATS')]")
        add_to_vacancy_in_ats_button.click()

    @retry_if_exception(NoSuchElementException)
    def select_vacancy(self):
        dropdown_input = self.driver.find_element_by_css_selector('input.vacancy-dropdown__input')
        dropdown_input.click()

        vacancy_option = self.find_vacancy_option()
        if not vacancy_option:
            return False
        vacancy_option.click()
        return True

    def try_save_to_new_vacancy(self):
        try:
            save_to_ats_button = self.driver.\
                find_element_by_xpath("//button[contains(text(), 'Save to our ATS')]")
            save_to_ats_button.click()
            time.sleep(2)
            return True
        except NoSuchElementException:
            return False

    def check_profile_in_ats(self):
        profile_in_ats_link = self.driver. \
            find_elements_by_css_selector(
                'a.save-button.user-auth.profile-in-ats.LinkedinResume'
            )
        return True if profile_in_ats_link else False

    def check_signed_in_to_ats(self):
        signin_ats_button = self.driver.find_elements_by_css_selector(
                'a.save-button.sign-in-to-ats.LinkedinResume'
            )
        return False if signin_ats_button else True

    @retry_if_exception(NoSuchElementException)
    def press_save_to_ats_button(self):
        save_to_ats_button = self.driver. \
            find_element_by_css_selector(
                'a.save-button.user-auth.LinkedinResume'
            )
        save_to_ats_button.click()
        time.sleep(15)
        return True

    @retry_if_exception(NoSuchElementException)
    def find_vacancy_option(self):
        vacancies_options = self.driver.find_elements_by_css_selector(
            "span.vacancy-dropdown__autocomplete-option-text"
        )
        lower_vacancy = self.vacancy.lower()
        for option in vacancies_options:
            if lower_vacancy in option.text.lower():
                return option
        return None

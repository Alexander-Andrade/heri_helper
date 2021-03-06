from src.linkedin import LinkedinLogin
from src.cleverstaff.cleverstaff_login import CleverstaffLogin
from src.google.linkedin_google_search import LinkedinGoogleSearch
import settings
from src.cli import CliArgsValidator
from src.cli.cli_args_parser import CliArgsParser
from src.webdriver import DriverBuilder
from src.webdriver import ProxySetter
from src.google.linkedin_search_query_builder import LinkedinSearchQueryBuilder
from src.add_candidate_to_database import AddCandidateToDatabase
from urllib.parse import unquote
import time


if __name__ == '__main__':
    args = CliArgsParser().parse()

    validation_result = CliArgsValidator(args).validate()
    if validation_result.is_failure():
        print(validation_result.error)
        exit()

    driver = DriverBuilder.build()

    print(f'LinkedIn login with {settings.LINKEDIN_EMAIL}/'
          f'{settings.LINKEDIN_PASSWORD} ...')

    LinkedinLogin(driver=driver).login()

    proxy_set = ProxySetter.set(args.proxy)
    if proxy_set:
        print(f'Proxy {args.proxy} ...')
    else:
        print('No proxy')

    search_query = LinkedinSearchQueryBuilder(args.query).build()
    print(f'\nSearching candidates with query: {search_query} ...')
    search_result = LinkedinGoogleSearch(
        driver=driver,
        query=search_query,
        pages=args.pages.split(',')
    ).search()

    if search_result.is_failure():
        print(search_result.error)
        driver.quit()
        exit()

    linkedin_urls = search_result.data
    print(f'\nNext candidates was found on pages {args.pages}\n')
    for url in linkedin_urls:
        print(unquote(url))

    print(f'\nCleverStaff login with {settings.ATS_EMAIL}/'
          f'{settings.ATS_PASSWORD} ...')

    CleverstaffLogin(driver=driver).login()

    print(f"\nAdding candidates to vacancy '{args.vacancy}' ...")

    time.sleep(3)
    driver.get(linkedin_urls[0])
    input("Enable browser extension by"
          "\n1. pressing extension button"
          "\n2. page reloading"
          "\n3. Press Enter to continue...")

    for candidate_url in linkedin_urls:
        db_save_result = AddCandidateToDatabase(
            driver=driver,
            candidate_url=candidate_url,
            vacancy=args.vacancy
        ).add()
        if db_save_result.is_failure():
            print(db_save_result.error)
            time.sleep(10)
            driver.quit()
            exit()
        print(db_save_result.data)

    print(f"\nDone")
    driver.quit()

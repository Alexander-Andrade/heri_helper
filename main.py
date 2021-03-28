from linkedin_login import LinkedinLogin
from cleverstaff_login import CleverstaffLogin
from linkedin_google_search import LinkedinGoogleSearch
import settings
from cli_args_validator import CliArgsValidator
from cli_args_parser import CliArgsParser
from driver_builder import DriverBuilder
from proxy_setter import ProxySetter
from linkedin_search_query_builder import LinkedinSearchQueryBuilder
from add_candidate_to_database import AddCandidateToDatabase


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

    proxy_result = ProxySetter.set(args.proxy)
    print(proxy_result.data)

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
        print(url)

    print(f'\nCleverStaff login with {settings.ATS_EMAIL}/'
          f'{settings.ATS_PASSWORD} ...')

    CleverstaffLogin(
        driver=driver,
        load_cookies=args.load_cookies,
        store_cookies=args.store_cookies
    ).login()

    print(f"\nAdding candidates to vacancy '{args.vacancy}' ...")

    for candidate_url in linkedin_urls:
        db_save_result = AddCandidateToDatabase(
            driver=driver,
            candidate_url=candidate_url,
            vacancy=args.vacancy
        ).add()
        if db_save_result.is_failure():
            print(db_save_result.error)
            driver.quit()
            exit()

    print(f"\nDone")
    driver.quit()

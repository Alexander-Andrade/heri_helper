from args import Args
from driver_builder import DriverBuilder
import settings
from linkedin_login import LinkedinLogin
from proxy_setter import ProxySetter
from cli_args_validator import CliArgsValidator
from cleverstaff_login import CleverstaffLogin
from linkedin_search_query_builder import LinkedinSearchQueryBuilder
from linkedin_google_search import LinkedinGoogleSearch
from add_candidate_to_database import AddCandidateToDatabase
from random import sample
from urllib.parse import unquote
import time

REST = [
    'Coffee break, baby ;) ? ',
    'Is Dobby free ?',
    'I will be back ?',
    'I can have a rest ?',
    'Can I sleep a bit ?',
    'Stop hunting for a little may be ?'
]

if __name__ == '__main__':
    driver = DriverBuilder.build()

    print(f'LinkedIn login with {settings.LINKEDIN_EMAIL}/'
          f'{settings.LINKEDIN_PASSWORD} ...')
    LinkedinLogin(driver=driver).login()

    print(f'\nCleverStaff login with {settings.ATS_EMAIL}/'
          f'{settings.ATS_PASSWORD} ...')
    CleverstaffLogin(driver=driver).login()
    input("Enable browser extension by"
          "\n1. pressing extension button"
          "\n2. page reloading"
          "\n3. Press Enter to continue...")

    while True:
        query = input('Enter query eg. "python developer" AND "London"\n')
        pages = input('Enter pages eg. 1,2\n')
        proxy = input('Enter proxy eg. 192.0.2.146:80'
                      ' to skip press Enter ;)\n')
        vacancy = input('Enter vacancy eg. Senior Full Stack Developer (Platform)\n')

        args = Args(query=query, pages=pages, proxy=proxy, vacancy=vacancy)

        validation_result = CliArgsValidator(args).validate()
        if validation_result.is_failure():
            print(validation_result.error)
            continue

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
            continue

        linkedin_urls = search_result.data
        print(f'\nNext candidates was found on pages {args.pages}\n')
        for url in linkedin_urls:
            print(unquote(url))

        print(f"\nAdding candidates to vacancy '{args.vacancy}' ...")

        for candidate_url in linkedin_urls:
            db_save_result = AddCandidateToDatabase(
                driver=driver,
                candidate_url=candidate_url,
                vacancy=args.vacancy
            ).add()
            if db_save_result.is_failure():
                print(db_save_result.error)
                time.sleep(10)
                continue
            print(db_save_result.data)

        stop = input(f"{sample(REST, 1)[0]} (y/n or CTRL+C) \n")
        if stop == 'y':
            break

        print(f"\nLeaving")
        driver.quit()

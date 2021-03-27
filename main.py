from selenium import webdriver
from login import LogIn
from linkedin_google_search import LinkedinGoogleSearch
import settings
from cli_args_validator import CliArgsValidator
from cli_args_parser import CliArgsParser


if __name__ == '__main__':
    args = CliArgsParser().parse()

    validation_result = CliArgsValidator(args).validate()
    if validation_result.is_failure():
        print(validation_result.error)
        exit()

    driver = webdriver.Chrome(settings.CHROME_DRIVER_PATH)
    LogIn(driver).login()

    if args.proxy:
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": args.proxy,
            "ftpProxy": args.proxy,
            "sslProxy": args.proxy,
            "proxyType": "MANUAL",

        }

    print(f'\nSearching candidates...')
    search_query = f"site:linkedin.com/in/ AND {args.query}"
    search_result = LinkedinGoogleSearch(
        driver=driver,
        query=search_query,
        pages=args.pages.split(',')
    ).search()

    if search_result.is_failure():
        print(search_result.error)
        exit()

    linkedin_urls = search_result.data
    print(f'\nNext candidates was found on pages {args.pages}\n')
    for url in linkedin_urls:
        print(url)

    print(f'\nAdding candidates to the database...')

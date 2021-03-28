import argparse


class CliArgsParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="$ python main.py "
                        "-q '\"python developer\" AND \"London\"' "
                        "-p '4,5'"
                        "-x '192.0.2.146:80'"
                        "-v 'Senior Full Stack Developer (Platform)'"
            )

    def parse(self):
        self.add_query_argument()
        self.add_pages_argument()
        self.add_proxy_argument()
        self.add_vacancy_argument()
        self.add_store_cookie_argument()
        self.add_load_cookie_argument()

        return self.parser.parse_args()

    def add_query_argument(self):
        self.parser.add_argument(
            '-q',
            '--query',
            type=str,
            help='\'"python developer" AND "London"\''
        )

    def add_pages_argument(self):
        self.parser.add_argument(
            '-p',
            '--pages',
            type=str,
            help="'3,4'"
        )

    def add_proxy_argument(self):
        self.parser.add_argument(
            '-x',
            '--proxy',
            type=str,
            help="'192.0.2.146:80'"
        )

    def add_vacancy_argument(self):
        self.parser.add_argument(
            '-v',
            '--vacancy',
            type=str,
            help="'Senior Full Stack Developer (Platform)'"
        )

    def add_store_cookie_argument(self):
        self.parser.add_argument(
            '-s',
            '--store_cookies',
            dest='store_cookies',
            action='store_true',
            help="store cookies from the session"
        )
        self.parser.set_defaults(store_cookies=False)

    def add_load_cookie_argument(self):
        self.parser.add_argument(
            '-l',
            '--load_cookies',
            dest='load_cookies',
            action='store_true',
            help="load cookies from the session"
        )
        self.parser.set_defaults(load_cookies=False)

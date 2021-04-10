from src.result import Result
import validators
import settings


class CliArgsValidator:
    def __init__(self, args):
        self.args = args

    def validate(self):
        if not self.args.query:
            return Result.failure('Heri, provide please query'
                                  ' parameter or use --help ;)')
        result = self.validate_pages()
        if result.is_failure():
            return result

        result = self.validate_proxy()
        if result.is_failure():
            return result

        result = self.validate_engine()
        if result.is_failure():
            return result

        return Result.success()

    def validate_pages(self):
        if not self.args.pages:
            return Result.failure('Heri, provide please pages'
                                  ' parameter or use --help ;)')
        for page in self.args.pages.split(','):
            if not validators.between(int(page), min=1, max=settings.MAX_PAGE):
                return Result.failure(f"{page} page out of range,"
                                      f" max is {settings.MAX_PAGE}")
        return Result.success()

    def validate_proxy(self):
        if not self.args.proxy:
            return Result.success()
        try:
            host, port = self.args.proxy.split(':')
        except ValueError:
            return Result.failure('Port is not provided, may be "80"?'
                                  ' Proxy example: "142.250.75.14:80"')
        if self.args.proxy and not validators.ipv4(host):
            return Result.failure('Heri, provide please proxy like'
                                  ' "142.250.75.14:80" or use --help ;)')

        return Result.success()

    def validate_engine(self):
        if not self.args.engine:
            return Result.success()

        if self.args.engine not in ['g', 'l']:
            return Result.failure('Heri, provide please engine '
                                  'like "g" (Google) or "l" (Linkedin)')

        return Result.success()

import time


def retry_if_exceptions(error, pauses=[2, 4, 8]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = len(pauses) + 1
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except error:
                    if i != retries - 1:
                        time.sleep(pauses[i])

        return wrapper

    return decorator

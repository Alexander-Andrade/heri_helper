import time


def retry_if_exceptions(error, pauses=[2, 4, 8]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for pause in pauses:
                try:
                    return func(*args, **kwargs)
                except error:
                    time.sleep(pause)

        return wrapper

    return decorator

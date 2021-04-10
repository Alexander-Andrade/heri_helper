import time


def retry_if_exception(error, pauses=[2, 4, 8]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = len(pauses) + 1
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except error:
                    if i < retries - 1:
                        time.sleep(pauses[i])
                    else:
                        raise
        return wrapper

    return decorator


def retry_if_return_value(value, pauses=[2, 4, 8]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = len(pauses) + 1
            for i in range(retries):
                returned_value = func(*args, **kwargs)
                if returned_value == value:
                    if i < retries - 1:
                        time.sleep(pauses[i])
                        continue
                return returned_value
        return wrapper

    return decorator
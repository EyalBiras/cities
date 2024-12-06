import signal
from functools import wraps


def timeout(seconds: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def _handle_timeout(signum, frame):
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")

            signal.signal(signal.SIGALRM, _handle_timeout)

            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)

                signal.alarm(0)

                return result

            except TimeoutError as e:
                raise e

            finally:
                signal.alarm(0)

        return wrapper

    return decorator

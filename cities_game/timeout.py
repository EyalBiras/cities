import signal
from contextlib import contextmanager


@contextmanager
def timeout(seconds: int):
    def _handle_timeout(signum, frame):
        raise TimeoutError(f"Code block timed out after {seconds} seconds")

    signal.signal(signal.SIGALRM, _handle_timeout)
    signal.alarm(seconds)

    try:
        yield
    finally:
        signal.alarm(0)

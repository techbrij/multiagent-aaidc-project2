import time
import requests
from typing import Callable, Any
from requests.exceptions import (
    Timeout,
    ConnectionError,
    HTTPError,
    RequestException,
)

def with_retry(
    func: Callable[[], Any],
    max_retries: int = 3,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0,
) -> Any:
    """
    Executes a function with retry logic for timeout, rate limit,
    and connection-related errors.

    Args:
        func (Callable): Function that performs the request.
        max_retries (int): Maximum retry attempts.
        base_delay (float): Initial delay in seconds.
        backoff_factor (float): Exponential backoff multiplier.

    Returns:
        Any: Result of the function if successful.

    Raises:
        Exception: If retries are exhausted.
    """
    delay = base_delay

    for attempt in range(1, max_retries + 1):
        try:
            return func()

        except Timeout as e:
            error_type = "Timeout"

        except ConnectionError as e:
            error_type = "ConnectionError"

        except HTTPError as e:
            status = e.response.status_code if e.response else None

            # GitHub rate limit or abuse protection
            if status in (429, 403):
                error_type = f"RateLimit ({status})"
            else:
                raise

        except RequestException:
            raise

        if attempt == max_retries:
            raise RuntimeError(
                f"{error_type} after {max_retries} retries"
            )

        time.sleep(delay)
        delay *= backoff_factor

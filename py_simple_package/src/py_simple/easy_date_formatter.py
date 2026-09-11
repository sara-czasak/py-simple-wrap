"""
easy_date_formatter is meant to simplify getting formatted dates.
Built on top of the datetime module — no more memorizing strftime codes.
"""

from datetime import datetime, timedelta


# ── Format registry (strftime pattern → readable name) ──────────────
_FORMATS = {
    "pretty": "%A, %B %d, %Y",
    "dd-mm-yyyy": "%d-%m-%Y",
    "mm-dd-yyyy": "%m-%d-%Y",
    "dd/mm/yyyy": "%d/%m/%Y",
    "mm/dd/yyyy": "%m/%d/%Y",
}


def list_available_formats():
    """
    Returns the supported format names for reference.

    Returns:
        list[str]: Names of every format key this module supports
            (e.g. 'pretty', 'dd-mm-yyyy', 'mm/dd/yyyy').

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import list_available_formats

            formats = list_available_formats()
            # -> ['pretty', 'dd-mm-yyyy', 'mm-dd-yyyy', 'dd/mm/yyyy', 'mm/dd/yyyy']
            ```

        === "The Traditional Way"
            ```python
            # There's no built-in equivalent — you'd have to keep
            # your own list of strftime patterns to remember them.
            formats = ["%A, %B %d, %Y", "%d-%m-%Y", "%m-%d-%Y"]
            ```
    """
    return list(_FORMATS.keys())


def _format_date(date_obj, fmt_key: str) -> str:
    """Apply a named format to a datetime object."""
    return date_obj.strftime(_FORMATS[fmt_key])


def _get_past_date(num_days_ago: int):
    """Calculate and return a past date."""
    return datetime.now() - timedelta(days=num_days_ago)


def _get_future_date(num_days_from_now: int):
    """Calculate and return a future date."""
    return datetime.now() + timedelta(days=num_days_from_now)


# ── Pretty dates ────────────────────────────────────────────────────


def get_pretty_date():
    """
    Returns the current date in a human-friendly format.

    Returns:
        str: Current date formatted as 'Weekday, Month Day, Year'
             (e.g., 'Monday, July 20, 2026').

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_pretty_date

            today = get_pretty_date()  # -> "Friday, July 31, 2026"
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime

            today = datetime.now().strftime("%A, %B %d, %Y")
            ```
    """
    return _format_date(datetime.now(), "pretty")


def get_past_pretty_date(num_days_ago: int):
    """
    Calculates a date from the past in pretty format.

    Args:
        num_days_ago (int): Number of days to subtract from today.

    Returns:
        str: Past date as 'Weekday, Month Day, Year'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_past_pretty_date

            last_week = get_past_pretty_date(7)
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime, timedelta

            last_week = (datetime.now() - timedelta(days=7)).strftime(
                "%A, %B %d, %Y"
            )
            ```
    """
    return _format_date(_get_past_date(num_days_ago), "pretty")


def get_future_pretty_date(num_days_from_now: int):
    """
    Calculates a future date in pretty format.

    Args:
        num_days_from_now (int): Number of days to add to today.

    Returns:
        str: Future date as 'Weekday, Month Day, Year'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_future_pretty_date

            next_week = get_future_pretty_date(7)
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime, timedelta

            next_week = (datetime.now() + timedelta(days=7)).strftime(
                "%A, %B %d, %Y"
            )
            ```
    """
    return _format_date(_get_future_date(num_days_from_now), "pretty")


# ── Hyphenated formats (DD-MM-YYYY or MM-DD-YYYY) ───────────────────


def dd_mm_yyyy():
    """
    Returns the current date in 'DD-MM-YYYY' format.

    Returns:
        str: Current date as 'DD-MM-YYYY' (e.g., '20-07-2026').

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import dd_mm_yyyy

            today = dd_mm_yyyy()  # -> "31-07-2026"
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime

            today = datetime.now().strftime("%d-%m-%Y")
            ```
    """
    return _format_date(datetime.now(), "dd-mm-yyyy")


def past_dd_mm_yyyy(num_days_ago: int):
    """
    Returns a past date in 'DD-MM-YYYY' format.

    Args:
        num_days_ago (int): Number of days to subtract from today.

    Returns:
        str: Past date as 'DD-MM-YYYY'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import past_dd_mm_yyyy

            last_week = past_dd_mm_yyyy(7)
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime, timedelta

            last_week = (datetime.now() - timedelta(days=7)).strftime(
                "%d-%m-%Y"
            )
            ```
    """
    return _format_date(_get_past_date(num_days_ago), "dd-mm-yyyy")


def future_dd_mm_yyyy(num_days_from_now: int):
    """
    Returns a future date in 'DD-MM-YYYY' format.

    Args:
        num_days_from_now (int): Number of days to add to today.

    Returns:
        str: Future date as 'DD-MM-YYYY'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import future_dd_mm_yyyy

            next_week = future_dd_mm_yyyy(7)
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime, timedelta

            next_week = (datetime.now() + timedelta(days=7)).strftime(
                "%d-%m-%Y"
            )
            ```
    """
    return _format_date(_get_future_date(num_days_from_now), "dd-mm-yyyy")


def mm_dd_yyyy():
    """
    Returns the current date in 'MM-DD-YYYY' format.

    Returns:
        str: Current date as 'MM-DD-YYYY' (e.g., '07-31-2026').

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import mm_dd_yyyy

            today = mm_dd_yyyy()  # -> "07-31-2026"
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime

            today = datetime.now().strftime("%m-%d-%Y")
            ```
    """
    return _format_date(datetime.now(), "mm-dd-yyyy")


def past_mm_dd_yyyy(num_days_ago: int):
    """
    Returns a past date in 'MM-DD-YYYY' format.

    Args:
        num_days_ago (int): Number of days to subtract from today.

    Returns:
        str: Past date as 'MM-DD-YYYY'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import past_mm_dd_yyyy

            last_week = past_mm_dd_yyyy(7)
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime, timedelta

            last_week = (datetime.now() - timedelta(days=7)).strftime(
                "%m-%d-%Y"
            )
            ```
    """
    return _format_date(_get_past_date(num_days_ago), "mm-dd-yyyy")


def future_mm_dd_yyyy(num_days_from_now: int):
    """
    Returns a future date in 'MM-DD-YYYY' format.

    Args:
        num_days_from_now (int): Number of days to add to today.

    Returns:
        str: Future date as 'MM-DD-YYYY'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import future_mm_dd_yyyy

            next_week = future_mm_dd_yyyy(7)
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime, timedelta

            next_week = (datetime.now() + timedelta(days=7)).strftime(
                "%m-%d-%Y"
            )
            ```
    """
    return _format_date(_get_future_date(num_days_from_now), "mm-dd-yyyy")


# ── Slashed formats (DD/MM/YYYY or MM/DD/YYYY) ──────────────────────


def slash_dd_mm_yyyy():
    """
    Returns the current date in 'DD/MM/YYYY' format.

    Returns:
        str: Current date as 'DD/MM/YYYY' (e.g., '31/07/2026').

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import slash_dd_mm_yyyy

            today = slash_dd_mm_yyyy()  # -> "31/07/2026"
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime

            today = datetime.now().strftime("%d/%m/%Y")
            ```
    """
    return _format_date(datetime.now(), "dd/mm/yyyy")


def past_slash_dd_mm_yyyy(num_days_ago: int):
    """
    Returns a past date in 'DD/MM/YYYY' format.

    Args:
        num_days_ago (int): Number of days to subtract from today.

    Returns:
        str: Past date as 'DD/MM/YYYY'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import past_slash_dd_mm_yyyy

            last_week = past_slash_dd_mm_yyyy(7)
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime, timedelta

            last_week = (datetime.now() - timedelta(days=7)).strftime(
                "%d/%m/%Y"
            )
            ```
    """
    return _format_date(_get_past_date(num_days_ago), "dd/mm/yyyy")


def future_slash_dd_mm_yyyy(num_days_from_now: int):
    """
    Returns a future date in 'DD/MM/YYYY' format.

    Args:
        num_days_from_now (int): Number of days to add to today.

    Returns:
        str: Future date as 'DD/MM/YYYY'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import future_slash_dd_mm_yyyy

            next_week = future_slash_dd_mm_yyyy(7)
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime, timedelta

            next_week = (datetime.now() + timedelta(days=7)).strftime(
                "%d/%m/%Y"
            )
            ```
    """
    return _format_date(_get_future_date(num_days_from_now), "dd/mm/yyyy")


def slash_mm_dd_yyyy():
    """
    Returns the current date in 'MM/DD/YYYY' format.

    Returns:
        str: Current date as 'MM/DD/YYYY' (e.g., '07/31/2026').

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import slash_mm_dd_yyyy

            today = slash_mm_dd_yyyy()  # -> "07/31/2026"
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime

            today = datetime.now().strftime("%m/%d/%Y")
            ```
    """
    return _format_date(datetime.now(), "mm/dd/yyyy")


def past_slash_mm_dd_yyyy(num_days_ago: int):
    """
    Returns a past date in 'MM/DD/YYYY' format.

    Args:
        num_days_ago (int): Number of days to subtract from today.

    Returns:
        str: Past date as 'MM/DD/YYYY'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import past_slash_mm_dd_yyyy

            last_week = past_slash_mm_dd_yyyy(7)
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime, timedelta

            last_week = (datetime.now() - timedelta(days=7)).strftime(
                "%m/%d/%Y"
            )
            ```
    """
    return _format_date(_get_past_date(num_days_ago), "mm/dd/yyyy")


def future_slash_mm_dd_yyyy(num_days_from_now: int):
    """
    Returns a future date in 'MM/DD/YYYY' format.

    Args:
        num_days_from_now (int): Number of days to add to today.

    Returns:
        str: Future date as 'MM/DD/YYYY'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import future_slash_mm_dd_yyyy

            next_week = future_slash_mm_dd_yyyy(7)
            ```

        === "The Traditional Way"
            ```python
            from datetime import datetime, timedelta

            next_week = (datetime.now() + timedelta(days=7)).strftime(
                "%m/%d/%Y"
            )
            ```
    """
    return _format_date(_get_future_date(num_days_from_now), "mm/dd/yyyy")

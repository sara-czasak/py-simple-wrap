"""
easy_validator is built to simplify validation.
"""
import re
from string import punctuation
import json


def is_valid_email(email: str) -> bool:
    """
    Returns true if email is valid.

    Arguments:
        email (str): email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_valid_email

            if is_valid_email("hello@world.com"):
                print("Looks good!")
            ```

        === "The Traditional Way"
            ```python
            import re

            pattern = r'[a-zA-Z_.%+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z]+'
            if re.fullmatch(pattern, "hello@world.com"):
                print("Looks good!")
            ```
    """
    pattern = r'[a-zA-Z_.%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+'
    return bool(re.fullmatch(pattern, email))


def is_valid_username(username: str) -> bool:
    """
    Returns true if username is valid.

    Arguments:
        username (str): username to validate.

    Returns:
        bool: True if the username is valid, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_valid_username

            result = is_valid_username("user_name")  # -> True
            ```

        === "The Traditional Way"
            ```python
            import re

            pattern = r'^[a-zA-Z0-9_]+'
            result = bool(re.fullmatch(pattern, "user_name"))
            ```
    """
    pattern = r'^[a-zA-Z0-9_]+'
    return bool(re.fullmatch(pattern, username))


def is_valid_zipcode(zipcode: int) -> bool:
    """
    Returns true if US zip code is valid.

    Arguments:
        zipcode (int): US zipcode to validate.

    Returns:
        bool: True if the zip code is valid, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_valid_zipcode

            result = is_valid_zipcode(12345)  # -> True
            ```

        === "The Traditional Way"
            ```python
            import re

            pattern = r'^[0-9]{5}$'
            result = bool(re.fullmatch(pattern, str(12345)))
            ```
    """
    pattern = r'^[0-9]{5}$'
    return bool(re.fullmatch(pattern, str(zipcode)))


def is_valid_url(url: str) -> bool:
    r"""
    Returns true if url is valid.

    Arguments:
        url (str): URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_valid_url

            result = is_valid_url("www.google.com")  # -> True
            ```

        === "The Traditional Way"
            ```python
            import re

            pattern = (r'(?:https?://(?:www\.)?|www\.)[a-zA-Z0-9-]+\.'
               r'(?:(?:[a-zA-Z0-9-]+\.)*)?(?:(?:[a-zA-Z0-9-]+\\)*)'
               r'?[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?(?:/\S*)?')
            result = bool(re.fullmatch(pattern, "www.google.com"))
            ```
    """
    pattern = (r'(?:https?://(?:www\.)?|www\.)[a-zA-Z0-9-]+\.'
               r'(?:(?:[a-zA-Z0-9-]+\.)*)?(?:(?:[a-zA-Z0-9-]+\\)*)'
               r'?[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?(?:/\S*)?')
    return bool(re.fullmatch(pattern, url))


def is_password_secure(password: str) -> bool:
    """
    Returns true if password is valid.

    Validation checks:
        - minimum length of 8 characters
        - at least one special character
        - at least one upper case letter
        - at least two lowercase letters
        - at least two digits
        - no repeating characters

    Arguments:
        password (str): password to validate.

    Returns:
        bool: True if the password meets all checks, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_password_secure

            result = is_password_secure("1andkrf!AG5")  # -> True
            ```

        === "The Traditional Way"
            ```python
            from string import punctuation

            password = "1andkrf!AG5"
            min_length = 8
            upper_letters = 0
            lower_letters = 0
            digits = 0
            special_characters = 0
            last_char = ''
            result = False

            if len(password) > min_length:
                for char in password:
                    if char.isdigit():
                        digits += 1
                        if char == last_char:
                            result = False
                            break
                        last_char = char
                    elif char.isalpha():
                        if char.upper() == char:
                            upper_letters += 1
                            if char == last_char:
                                result = False
                                break
                            last_char = char
                        elif char.lower() == char:
                            lower_letters += 1
                            if char == last_char:
                                result = False
                                break
                            last_char = char
                    elif char in punctuation:
                        special_characters += 1
                        if char == last_char:
                            result = False
                            break
                        last_char = char
                else:
                    result = (
                        upper_letters >= 1 and lower_letters >= 2 and
                        digits >= 2 and special_characters >= 1
                    )
            ```
    """
    min_length = 8
    upper_letters = 0
    lower_letters = 0
    digits = 0
    special_characters = 0
    last_char = ''

    if len(password) > min_length:
        for char in password:
            if char.isdigit():
                digits += 1
                if char == last_char:
                    return False
                else:
                    last_char = char
            elif char.isalpha():
                if char.upper() == char:
                    upper_letters += 1
                    if char == last_char:
                        return False
                    else:
                        last_char = char
                elif char.lower() == char:
                    lower_letters += 1
                    if char == last_char:
                        return False
                    else:
                        last_char = char
            elif char in punctuation:
                special_characters += 1
                if char == last_char:
                    return False
                else:
                    last_char = char
            else:
                pass
        if (upper_letters >= 1 and lower_letters >= 2 and digits >= 2 and
                special_characters >= 1):
            return True
        else:
            return False
    else:
        return False


def is_valid_creditcard(card_num: str):
    r"""
    Returns true if the credit card number is valid according to the Luhn algorithm. (https://en.wikipedia.org/wiki/Luhn_algorithm)

    Arguments:
        card_num (str): The credit card number. Valid strings are 13 to 19 digits long, with optional dashes or spaces.

    Returns:
        bool: True if the credit card number is valid, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_valid_creditcard

            result = is_valid_creditcard("4242-4242-4242-4242")  # -> True
            ```

        === "The Traditional Way"
            ```python
            import re

            card_num = card_num.replace("-", "").replace(" ", "")
            pattern = r"[0-9]{13,19}"

            if not re.fullmatch(pattern, card_num):
                return False

            digits = [int(digit) for digit in card_num]
            reversed_digits = reversed(digits)

            sum = 0
            for index, digit in enumerate(reversed_digits):
                if index % 2 == 0:
                    # every other digit, starting with the last
                    sum += digit
                else:
                    doubled = 2 * digit
                    sum += doubled if doubled < 10 else doubled - 9

            return sum % 10 == 0
            ```
    """

    card_num = card_num.replace("-", "").replace(" ", "")
    pattern = r"[0-9]{13,19}"

    if not re.fullmatch(pattern, card_num):
        return False

    digits = [int(digit) for digit in card_num]
    reversed_digits = reversed(digits)

    sum = 0
    for index, digit in enumerate(reversed_digits):
        if index % 2 == 0:
            # every other digit, starting with the last
            sum += digit
        else:
            doubled = 2 * digit
            sum += doubled if doubled < 10 else doubled - 9

    return sum % 10 == 0


def is_valid_phone_number(phone_number: str) -> bool:
    r"""
    Returns true if the phone number is a valid US-style phone number.

    Accepts an optional leading "+1" country code, an optional area code
    in parentheses, and digit groups separated by spaces, dashes, or dots
    (or no separator at all).

    Args:
        phone_number (str): The phone number to validate.

    Returns:
        bool: True if the phone number is valid, False otherwise.

    Example:
        === "The Py_simple Way"
```python
            from py_simple import is_valid_phone_number

            result = is_valid_phone_number("(123) 456-7890")  # -> True
```

        === "The Traditional Way"
```python
            import re

            pattern = r'^(\+1[\s.-]?)?(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}$'
            result = bool(re.fullmatch(pattern, "(123) 456-7890"))
```
    """
    pattern = r'^(\+1[\s.-]?)?(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}$'
    return bool(re.fullmatch(pattern, phone_number))
def is_valid_json(json_string: str) -> bool:
    r"""
    Returns true if the string is valid JSON.
 
    Arguments:
        json_string (str): the string to validate.
 
    Returns:
        bool: True if the string parses as valid JSON, False otherwise.
 
    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_valid_json
 
            result = is_valid_json('{"key": "value"}')  # -> True
            ```
 
        === "The Traditional Way"
            ```python
            import json
 
            try:
                json.loads('{"key": "value"}')
                result = True
            except (ValueError, TypeError):
                result = False
            ```
    """
    try:
        json.loads(json_string)
        return True
    except (ValueError, TypeError):
        return False
 
 
def is_valid_ipv4(ip: str) -> bool:
    r"""
    Returns true if the string is a valid IPv4 address.
 
    Arguments:
        ip (str): the IP address to validate.
 
    Returns:
        bool: True if the IP address is valid, False otherwise.
 
    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_valid_ipv4
 
            result = is_valid_ipv4("192.168.1.1")  # -> True
            ```
 
        === "The Traditional Way"
            ```python
            pattern = r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})'
            match = re.fullmatch(pattern, "192.168.1.1")
            result = bool(match) and all(0 <= int(g) <= 255 for g in match.groups())
            ```
    """
    pattern = r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})'
    match = re.fullmatch(pattern, ip)
 
    if not match:
        return False
 
    # regex only checks digit count, not range or leading zeros
    for octet in match.groups():
        if len(octet) > 1 and octet[0] == '0':
            return False
        if not 0 <= int(octet) <= 255:
            return False
 
    return True


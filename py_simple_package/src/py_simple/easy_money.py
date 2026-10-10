"""
easy_money formats prices and splits bills without the decimal boilerplate.
"""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


class EasyMoneyError(Exception):
    """
    Raised when a money calculation cannot be completed.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def _as_money(amount) -> Decimal:
    if isinstance(amount, bool) or not isinstance(amount, (int, float, str, Decimal)):
        raise EasyMoneyError("\n\nERROR: amount must be a number.")
    try:
        return Decimal(str(amount))
    except InvalidOperation as error:
        raise EasyMoneyError(f"\n\nERROR: {error}") from None


def _cents(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def format_money(amount, symbol: str = "$") -> str:
    """
    Format a number as money with two decimal places.

    Args:
        amount: The amount to format.
        symbol (str, optional): Currency symbol placed before the number.
            Defaults to `"$"`.

    Returns:
        str: The formatted amount, such as `"$12.50"`.

    Raises:
        EasyMoneyError: If `amount` is not a number.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import format_money

            print(format_money(12.5))
            ```

        === "The Traditional Way"
            ```python
            from decimal import Decimal, ROUND_HALF_UP

            cents = Decimal("12.5").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            print(f"${cents}")
            ```
    """
    return f"{symbol}{_cents(_as_money(amount))}"


def add_tax(amount, rate: float) -> float:
    """
    Add a tax rate to an amount and round to cents.

    Args:
        amount: The price before tax.
        rate (float): Tax rate as a percent, such as `8.5` for 8.5%.

    Returns:
        float: The price after tax, rounded to two decimal places.

    Raises:
        EasyMoneyError: If `amount` or `rate` is not a number, or if
            `rate` is negative.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import add_tax

            total = add_tax(10, 8.5)
            ```

        === "The Traditional Way"
            ```python
            from decimal import Decimal, ROUND_HALF_UP

            total = (Decimal("10") * (1 + Decimal("8.5") / 100)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            ```
    """
    price = _as_money(amount)
    tax_rate = _as_money(rate)
    if tax_rate < 0:
        raise EasyMoneyError("\n\nERROR: tax rate cannot be negative.")
    total = price * (1 + tax_rate / Decimal(100))
    return float(_cents(total))


def split_bill(total, people: int) -> float:
    """
    Split a bill evenly and round each share to cents.

    Args:
        total: The full bill.
        people (int): How many people are paying. Must be at least 1.

    Returns:
        float: One person's share, rounded to two decimal places.

    Raises:
        EasyMoneyError: If `people` is less than 1 or `total` is not a
            number.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import split_bill

            share = split_bill(48, 3)
            ```

        === "The Traditional Way"
            ```python
            from decimal import Decimal, ROUND_HALF_UP

            share = (Decimal("48") / 3).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            ```
    """
    if isinstance(people, bool) or not isinstance(people, int) or people < 1:
        raise EasyMoneyError("\n\nERROR: people must be an integer of at least 1.")
    share = _as_money(total) / Decimal(people)
    return float(_cents(share))

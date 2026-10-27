"""
easy_money formats prices and splits bills without the decimal boilerplate.
"""

from decimal import Decimal, DecimalException, InvalidOperation, ROUND_HALF_UP


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
        raise EasyMoneyError("\n\nERROR: amount must be a number.") from None
    try:
        value = Decimal(str(amount))
    except InvalidOperation as error:
        raise EasyMoneyError(f"\n\nERROR: {error}") from None
    if not value.is_finite():
        raise EasyMoneyError("\n\nERROR: amount must be finite.") from None
    return value


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
        EasyMoneyError: If `amount` is not a finite number.

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


def add_tax(amount, rate: float) -> Decimal:
    """
    Add a tax rate to an amount and round to cents.

    Args:
        amount: The price before tax.
        rate (float): Tax rate as a percent, such as `8.5` for 8.5%.

    Returns:
        Decimal: The price after tax, rounded to two decimal places.

    Raises:
        EasyMoneyError: If `amount` or `rate` is not a finite number, or if
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
        raise EasyMoneyError("\n\nERROR: tax rate cannot be negative.") from None
    total = price * (1 + tax_rate / Decimal(100))
    return _cents(total)


def calculate_discount(amount, discount_rate: float) -> Decimal:
    """
    Calculate the price after applying a percentage discount.

    Args:
        amount: The original price before the discount.
        discount_rate (float): Discount percentage, such as `15` for 15%.

    Returns:
        Decimal: The discounted price, rounded to two decimal places.

    Raises:
        EasyMoneyError: If the amount or discount rate is not a finite number,
            or if the discount rate is outside the range of 0 to 100.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import calculate_discount

            discounted_price = calculate_discount(2000, 15)
            ```

        === "The Traditional Way"
            ```python
            from decimal import Decimal, ROUND_HALF_UP

            amount = Decimal("2000")
            discount_rate = Decimal("15")
            discounted_price = (amount * (1 - discount_rate / 100)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            ```
    """
    price = _as_money(amount)
    discount = _as_money(discount_rate)

    if discount < 0 or discount > 100:
        raise EasyMoneyError(
            "\n\nERROR: discount rate must be between 0 and 100."
        ) from None

    discounted_price = price * (1 - discount / Decimal(100))

    return _cents(discounted_price)


def calculate_tip(amount, tip_rate: float) -> Decimal:
    """
    Calculate the tip amount for a bill given a percentage rate.

    Args:
        amount: The bill amount before tip.
        tip_rate (float): Tip percentage, such as `15` or `20` for 15% or 20%.

    Returns:
        Decimal: The tip amount to add, rounded to two decimal places.

    Raises:
        EasyMoneyError: If `amount` or `tip_rate` is not a finite number,
            or if `tip_rate` is negative.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import calculate_tip

            tip = calculate_tip(50, 18)
            ```

        === "The Traditional Way"
            ```python
            from decimal import Decimal, ROUND_HALF_UP

            bill = Decimal("50")
            rate = Decimal("18")
            tip = (bill * (rate / Decimal(100))).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            ```
    """
    price = _as_money(amount)
    tip = _as_money(tip_rate)
    if tip < 0:
        raise EasyMoneyError("\n\nERROR: tip rate cannot be negative.") from None
    tip_amount = price * (tip / Decimal(100))
    return _cents(tip_amount)


def split_bill(total, people: int) -> Decimal:
    """
    Split a bill evenly and round each share to cents.

    Args:
        total: The full bill.
        people (int): How many people are paying. Must be at least 1.

    Returns:
        Decimal: One person's share, rounded to two decimal places.

    Raises:
        EasyMoneyError: If `people` is less than 1 or `total` is not a
            finite number.

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
        raise EasyMoneyError(
            "\n\nERROR: people must be an integer of at least 1."
        ) from None
    share = _as_money(total) / Decimal(people)
    return _cents(share)


def split_bill_exact(total, people: int) -> list[Decimal]:
    """
    Splits a bill into cent-precise shares that preserve the rounded total.

    Rounds the full bill once using ROUND_HALF_UP, then gives leftover
    cents to the first shares. Shares differ by at most one cent. Refunds
    use the same allocation with negative shares; zero shares are 0.00.
    Existing split_bill still returns one independently rounded share.

    Args:
        total (int | float | str | Decimal): Finite amount. Floats are
            converted through their string representation.
        people (int): Number of shares. Must be at least 1; booleans and
            non-integers are not accepted.

    Returns:
        list[Decimal]: Exactly `people` shares with two decimal places.
            For example, 10 split three ways gives 3.34, 3.33 and 3.33.

    Raises:
        EasyMoneyError: If the amount/count is invalid or rounding cannot
            be completed in the current Decimal context.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import split_bill_exact

            shares = split_bill_exact("10.00", 3)
            print(shares)  # [Decimal('3.34'), Decimal('3.33'), Decimal('3.33')]
            print(sum(shares))  # 10.00
            ```

        === "The Traditional Way"
            ```python
            from decimal import Decimal, ROUND_HALF_UP

            total, people = Decimal("10.00"), 3
            rounded = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            numerator, denominator = rounded.as_integer_ratio()
            cents = abs(numerator) * 100 // denominator
            base, remainder = divmod(cents, people)
            sign = -1 if rounded < 0 else 1
            shares = []
            for i in range(people):
                cent_share = Decimal(sign * (base + (i < remainder)))
                parts = cent_share.as_tuple()
                shares.append(Decimal((parts.sign, parts.digits, -2)))
            print(shares)  # [Decimal('3.34'), Decimal('3.33'), Decimal('3.33')]
            print(sum(shares))  # 10.00
            ```
    """
    if isinstance(people, bool) or not isinstance(people, int) or people < 1:
        raise EasyMoneyError(
            "\n\nERROR: people must be an integer of at least 1."
        ) from None
    try:
        amount = _as_money(total)
        rounded = _cents(amount)
        # Allocate whole cents without rounding the division or using floats.
        numerator, denominator = rounded.as_integer_ratio()
        cents = abs(numerator) * 100 // denominator
        base, remainder = divmod(cents, people)
        sign = -1 if rounded < 0 else 1
        shares = []
        for index in range(people):
            # Construct cents directly; context clamping must not add decimals.
            cent_share = Decimal(sign * (base + (index < remainder)))
            parts = cent_share.as_tuple()
            shares.append(Decimal((parts.sign, parts.digits, -2)))
        return shares
    except (DecimalException, ValueError) as error:
        raise EasyMoneyError(f"\n\nERROR: {error}") from None

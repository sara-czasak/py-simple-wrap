"""Beginner-friendly helpers for common statistics operations."""

import math
from statistics import correlation as _correlation


def median(nums: list[float]) -> float:
    """
    Returns the middle value of a list of numbers.

    With an even count, the mean of the two middle values is returned.

    Args:
        nums (list[float]): List of numbers.

    Returns:
        float: The median value.

    Raises:
        ValueError: If the list is empty.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import median

            result = median([4, 1, 9, 2])  # -> 3.0
            ```

        === "The Traditional Way"
            ```python
            nums = sorted([4, 1, 9, 2])
            mid = len(nums) // 2
            result = nums[mid] if len(nums) % 2 else (nums[mid - 1] + nums[mid]) / 2
            ```
    """
    if not nums:
        raise ValueError("Cannot find the median of an empty list.")

    ordered = sorted(nums)
    mid = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def mode(nums: list[float]) -> float:
    """
    Returns the number that appears most often in a list.

    If several numbers tie, the one that appears first is returned.

    Args:
        nums (list[float]): List of numbers.

    Returns:
        float: The most frequent number.

    Raises:
        ValueError: If the list is empty.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import mode

            result = mode([2, 1, 2, 3])  # -> 2
            ```

        === "The Traditional Way"
            ```python
            from collections import Counter

            nums = [2, 1, 2, 3]
            result = Counter(nums).most_common(1)[0][0]
            ```
    """
    if not nums:
        raise ValueError("Cannot find the mode of an empty list.")

    return max(nums, key=nums.count)


def data_range(nums: list[float]) -> float:
    """
    Returns the difference between the largest and smallest numbers.

    Args:
        nums (list[float]): List of numbers.

    Returns:
        float: The difference between max and min.

    Raises:
        ValueError: If the list is empty.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import data_range

            result = data_range([4, 1, 8, 2])  # -> 7
            ```

        === "The Traditional Way"
            ```python
            nums = [4, 1, 8, 2]
            result = max(nums) - min(nums)
            ```
    """
    if not nums:
        raise ValueError("Cannot find the range of an empty list.")

    return max(nums) - min(nums)


def variance(nums: list[float]) -> float:
    """
    Returns how spread out the numbers are, as sample variance.

    Args:
        nums (list[float]): List of numbers.

    Returns:
        float: The sample variance, using n - 1 as the divisor.

    Raises:
        ValueError: If the list has fewer than two numbers.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import variance

            result = variance([1, 2, 3])  # -> 1.0
            ```

        === "The Traditional Way"
            ```python
            nums = [1, 2, 3]
            mean = sum(nums) / len(nums)
            result = sum((num - mean) ** 2 for num in nums) / (len(nums) - 1)
            ```
    """
    if len(nums) < 2:
        raise ValueError("Variance needs at least two numbers.")

    mean = sum(nums) / len(nums)
    return sum((num - mean) ** 2 for num in nums) / (len(nums) - 1)


def standard_deviation(nums: list[float]) -> float:
    """
    Returns how far numbers typically sit from the average.

    Args:
        nums (list[float]): List of numbers.

    Returns:
        float: The square root of the sample variance.

    Raises:
        ValueError: If the list has fewer than two numbers.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import standard_deviation

            result = standard_deviation([1, 2, 3])  # -> 1.0
            ```

        === "The Traditional Way"
            ```python
            from statistics import stdev

            nums = [1, 2, 3]
            result = stdev(nums)
            ```
    """
    if len(nums) < 2:
        raise ValueError("Standard deviation needs at least two numbers.")

    return math.sqrt(variance(nums))


def percentile(nums: list[float], percent: float) -> float:
    """
    Returns the value below which the given percent of numbers fall.

    Uses the nearest-rank method.

    Args:
        nums (list[float]): List of numbers.
        percent (float): The percentile, from 0 to 100.

    Returns:
        float: The value at the given percentile.

    Raises:
        ValueError: If the list is empty or percent is outside 0-100.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import percentile

            result = percentile([1, 2, 3, 4], 75)  # -> 3
            ```

        === "The Traditional Way"
            ```python
            import math

            nums, percent = [1, 2, 3, 4], 75
            ordered = sorted(nums)
            result = ordered[max(0, math.ceil(len(ordered) * percent / 100) - 1)]
            ```
    """
    if not nums:
        raise ValueError("Cannot find a percentile of an empty list.")
    if percent < 0 or percent > 100:
        raise ValueError("'percent' must be between 0 and 100.")

    ordered = sorted(nums)
    position = math.ceil(len(ordered) * percent / 100)
    return ordered[max(0, position - 1)]


def z_score(nums: list[float], value: float) -> float:
    """
        Returns how many standard deviations a value is from the average.

        A positive result means the value is above average, negative means
        below average.

        Args:
            nums (list[float]): List of numbers used to calculate the average
                and spread.
            value (float): The number to measure against the list.

        Returns:
            float: The z-score, rounded to 2 decimal places.

        Raises:
            ValueError: If the list has fewer than two numbers.

        Example:
            === "The Py_simple Way"
    ```python
                from py_simple import z_score

                result = z_score([1, 2, 3, 4, 5], 5)  # -> 1.26
    ```

            === "The Traditional Way"
    ```python
                from statistics import mean, stdev

                nums, value = [1, 2, 3, 4, 5], 5
                result = round((value - mean(nums)) / stdev(nums), 2)
    ```
    """
    if len(nums) < 2:
        raise ValueError("z_score needs at least two numbers.")

    mean = sum(nums) / len(nums)
    return round((value - mean) / standard_deviation(nums), 2)


def interquartile_range(nums: list[float]) -> float:
    """
        Returns the spread of the middle 50% of a list of numbers.

        This is the difference between the 75th percentile (Q3) and the
        25th percentile (Q1). Unlike variance or standard deviation, it
        isn't affected by extreme outliers.

        Args:
            nums (list[float]): List of numbers.

        Returns:
            float: The difference between the 75th and 25th percentiles.

        Raises:
            ValueError: If the list is empty.

        Example:
            === "The Py_simple Way"
    ```python
                from py_simple import interquartile_range

                result = interquartile_range([1, 2, 3, 4])  # -> 2
    ```

            === "The Traditional Way"
    ```python
                import math

                nums = [1, 2, 3, 4]
                ordered = sorted(nums)

                def _percentile(ordered, percent):
                    position = math.ceil(len(ordered) * percent / 100)
                    return ordered[max(0, position - 1)]

                result = _percentile(ordered, 75) - _percentile(ordered, 25)
    ```
    """
    if not nums:
        raise ValueError("Cannot find the interquartile range of an empty list.")

    return percentile(nums, 75) - percentile(nums, 25)


def correlation_coefficient(x: list[float], y: list[float]) -> float:
    """
    Returns Pearson's correlation coefficient for two lists of paired numbers.

    Uses Python's statistics module, with input checks and readable errors.

    Values at the same position must describe the same observation. For
    example, x[0] and y[0] could be one student's study hours and test score.
    Do not sort the lists independently, as this would change the pairs.

    A positive result means the values tend to increase together; a negative
    result means one tends to decrease as the other increases. A result near
    zero means little linear association, not necessarily no relationship.
    Correlation does not show that one variable causes changes in the other.

    Args:
        x (list[float]): First list of finite numbers (integers or floats).
        y (list[float]): Second list of finite numbers, in matching order.
            Both lists must have the same length and at least two values.
            Neither list can contain only one repeated value.

    Returns:
        float: Pearson's r, from -1.0 to 1.0, without rounding. Values of
            -1.0 and 1.0 indicate perfect negative and positive linear
            relationships, respectively.

    Raises:
        TypeError: If either list contains a value that is not a number.
        ValueError: If the lengths differ, there are fewer than two pairs,
            a value is NaN or infinite, or either list is constant.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import correlation_coefficient

            study_hours = [1, 2, 3, 4, 5]
            test_scores = [60, 65, 75, 70, 80]
            result = correlation_coefficient(study_hours, test_scores)
            print(round(result, 2))  # -> 0.9
            ```

        === "The Traditional Way"
            ```python
            from statistics import correlation

            study_hours = [1, 2, 3, 4, 5]
            test_scores = [60, 65, 75, 70, 80]
            result = correlation(study_hours, test_scores)
            print(round(result, 2))  # -> 0.9
            ```
    """
    if len(x) != len(y):
        raise ValueError("Both lists must have the same number of values.")
    if len(x) < 2:
        raise ValueError("Correlation needs at least two pairs of numbers.")

    for name, values in (("x", x), ("y", y)):
        if any(not isinstance(value, (int, float)) for value in values):
            raise TypeError(f"'{name}' must contain only numbers (integers or floats).")
        if any(not math.isfinite(value) for value in values):
            raise ValueError(f"'{name}' must not contain NaN or infinite values.")
        if all(value == values[0] for value in values):
            raise ValueError(
                f"'{name}' must contain at least two different values; "
                "correlation is undefined for a constant list."
            )

    # Positive scaling preserves correlation and avoids squaring very large
    # or very small values inside statistics.correlation.
    x_scale = max(abs(value) for value in x)
    y_scale = max(abs(value) for value in y)
    return _correlation(
        [value / x_scale for value in x],
        [value / y_scale for value in y],
    )

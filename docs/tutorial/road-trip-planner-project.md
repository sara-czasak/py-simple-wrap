# Build a Road Trip Route & Fuel Planner with Easy Converter and Easy Money

Combine **Easy Converter** and **Easy Money** to plan driving distances, estimate highway travel time, and split group road trip expenses cleanly.

## A small real-world example

Planning a getaway with friends usually means juggling metric conversions across borders, calculating driving hours from mileage, and figuring out who owes what for fuel and campsite bookings without awkward rounding errors.

Install the package with `python -m pip install py-simple-wrap`, then run:

```python
from py_simple import (
    calculate_discount,
    format_money,
    miles_to_km,
    seconds_to_hh_mm_ss,
    split_bill,
)

# 1. Plan a 350-mile road trip for 4 friends
route_miles = 350.0
route_km = miles_to_km(route_miles)

# 2. Highway driving at ~50 mph averages 7 hours = 25,200 seconds
drive_seconds = int((route_miles / 50.0) * 3600)
travel_time = seconds_to_hh_mm_ss(drive_seconds)

# 3. Fuel and campsite expenses
fuel_cost = 120.00
campsite_cost = 80.00
subtotal = fuel_cost + campsite_cost

# 4. Apply a 15% promotional discount on the campsite booking
trip_total = calculate_discount(subtotal, 15.0)

# 5. Split expenses evenly among 4 travelers
friends = 4
per_person = split_bill(trip_total, friends)

print(f"Road Trip Distance: {route_miles:.0f} miles ({route_km:.1f} km)")
print(f"Estimated Driving Time: {travel_time}")
print(f"Total Trip Expenses: {format_money(trip_total)}")
print(f"Share Per Person ({friends} friends): {format_money(per_person)}")
```

Example output:

```text
Road Trip Distance: 350 miles (563.3 km)
Estimated Driving Time: 7:00:00
Total Trip Expenses: $170.00
Share Per Person (4 friends): $42.50
```

## What happened?

1. `miles_to_km(350.0)` converts imperial distance into kilometers without having to memorize or look up `1.60934`.
2. `seconds_to_hh_mm_ss(drive_seconds)` converts raw seconds into a clear `HH:MM:SS` format.
3. `calculate_discount(subtotal, 15.0)` calculates the discounted total using accurate decimal arithmetic so fractional pennies don't get lost.
4. `split_bill(trip_total, friends)` divides the final bill evenly among all passengers, rounding accurately to standard cents.
5. `format_money(...)` returns formatted currency strings with the standard `$` symbol and two decimal places.

## Try it yourself

- Add a scenic detour by bumping `route_miles` to `480.0` and see how the travel time changes.
- Change currency symbols for an international journey by using `format_money(per_person, symbol="€")` or `format_money(per_person, symbol="£")`.
- Add another passenger to `friends` and watch `split_bill()` recompute everyone's fair share automatically.

## Why use these helpers?

Standard library Python requires writing manual conversion formulas (`miles * 1.609344`), formatting `timedelta` objects, and importing `decimal.Decimal` with custom `ROUND_HALF_UP` quantization context just to format currency without floating-point inaccuracies like `$42.50000000000001`. Combining `easy_converter` and `easy_money` turns multi-step arithmetic into clear, beginner-friendly functions that handle rounding and formatting safely out of the box.

Related tutorials:
- [Easy Converter Tutorial](easy_converter.md)
- [Easy Money Tutorial](easy_money.md)

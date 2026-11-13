# Build a Trail Stage Planner with Easy Converter and Easy Lists

Combine **Easy Converter** and **Easy Lists** to plan multi-day trail stages, convert distances and split times, and group legs into daily itineraries.

## A small real-world example

Hikers, trail runners, and bikepackers often plan multi-stage expeditions where trail guides publish distances in kilometers and split times in hours and minutes. If you are coordinating with international teammates or pacing your trek, you need to convert distances to miles, sum total moving time, identify shared camp hubs, and group stages into realistic daily chunks. This script runs entirely in memory without writing files to disk.

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save this as `trail_stage_planner.py`:

```python
from py_simple import (
    chunk_list,
    find_duplicates,
    hh_mm_ss_to_seconds,
    km_to_mile,
    seconds_to_hh_mm_ss,
    sum_all,
    unique_items,
)

stages = [
    {"name": "Pine Ridge", "km": 14.5, "time": (3, 45, 0)},
    {"name": "Crystal Creek", "km": 18.2, "time": (4, 30, 0)},
    {"name": "Eagle Summit", "km": 11.8, "time": (3, 15, 0)},
    {"name": "Mist Valley", "km": 15.5, "time": (4, 0, 0)},
]

waypoints = [
    "Trailhead",
    "Pine Ridge",
    "Base Camp",
    "Crystal Creek",
    "Base Camp",
    "Eagle Summit",
    "Mist Valley",
]

# 1. Identify distinct checkpoints and shared hub waypoints
distinct_stops = unique_items(waypoints)
repeated_hubs = find_duplicates(waypoints)

# 2. Calculate overall distance in kilometers and miles
total_km = sum_all([s["km"] for s in stages])
total_miles = km_to_mile(total_km)

# 3. Convert stage split durations and calculate total moving time
stage_seconds = [hh_mm_ss_to_seconds(*s["time"]) for s in stages]
total_seconds = sum_all(stage_seconds)
total_time = seconds_to_hh_mm_ss(total_seconds)

# 4. Divide stages into 2-stage daily itineraries
daily_itineraries = chunk_list(stages, 2)

print("--- Trail Expedition Plan ---")
print(f"Total distance: {total_km:.1f} km ({total_miles:.2f} miles)")
print(f"Total moving time: {total_time}")
print(f"Distinct waypoints ({len(distinct_stops)}): {distinct_stops}")
print(f"Shared hub waypoints: {repeated_hubs}")
print()
print("--- Daily Itineraries ---")
for day_idx, day_stages in enumerate(daily_itineraries, start=1):
    day_km = sum_all([s["km"] for s in day_stages])
    day_miles = km_to_mile(day_km)
    stage_names = ", ".join(s["name"] for s in day_stages)
    print(f"Day {day_idx} ({len(day_stages)} stages): {stage_names}")
    print(f"  Distance: {day_km:.1f} km ({day_miles:.2f} miles)")
```

Run the script from your terminal:

```bash
python trail_stage_planner.py
```

Example output:

```text
--- Trail Expedition Plan ---
Total distance: 60.0 km (37.28 miles)
Total moving time: 15:30:00
Distinct waypoints (6): ['Trailhead', 'Pine Ridge', 'Base Camp', 'Crystal Creek', 'Eagle Summit', 'Mist Valley']
Shared hub waypoints: ['Base Camp']

--- Daily Itineraries ---
Day 1 (2 stages): Pine Ridge, Crystal Creek
  Distance: 32.7 km (20.32 miles)
Day 2 (2 stages): Eagle Summit, Mist Valley
  Distance: 27.3 km (16.96 miles)
```

## What happened?

`unique_items()` removes duplicate stopovers from the route waypoint list while preserving their original travel order.

`find_duplicates()` extracts waypoints visited more than once, highlighting which campsites serve as recurring resupply hubs.

`sum_all()` adds up every stage distance without manual accumulator loops, returning the total expedition length.

`km_to_mile()` converts distance from kilometers into miles as a clean floating-point value rounded to two decimal places.

`hh_mm_ss_to_seconds()` translates individual stage split times given as hours, minutes, and seconds into total elapsed seconds so they can be summed accurately.

`seconds_to_hh_mm_ss()` formats the cumulative duration back into a human-readable `"hh:mm:ss"` moving time string.

`chunk_list()` partitions the sequence of stages into smaller lists of two stages each, creating manageable multi-stage daily itineraries.

## Try it yourself

- **Add a fifth stage:** Append a new leg like `{"name": "Sunset Ridge", "km": 13.0, "time": (3, 20, 0)}` to see `chunk_list()` automatically create a third day.
- **Track elevation gain:** Import `meters_to_feet` from `py_simple` and convert mountain pass elevations into feet alongside your stage distances.
- **Adjust daily pacing:** Change the chunk size in `chunk_list(stages, 3)` to schedule an ambitious 3-stage day instead.

## Why use these helpers?

Without `py-simple-wrap`, achieving this with Python's standard library requires juggling multiple modules and manual boilerplate:
- Performing unit arithmetic by multiplying conversion factors like `km * 0.621371` and rounding manually.
- Importing `datetime.timedelta` or writing integer division and modulo math (`seconds // 3600`, `(seconds % 3600) // 60`) just to turn split times into readable clock strings.
- Writing list comprehension slicing idioms (`[items[i:i + size] for i in range(0, len(items), size)]`) or importing `itertools` recipes to chunk lists.
- Maintaining dictionary counting loops or `set()` operations to filter unique and duplicate waypoints while attempting to preserve insertion order.

Combining `easy_converter` and `easy_lists` replaces conversion formulas and list slicing plumbing with clean, readable function calls.

For more examples and detailed function references, see [Easy Converter](easy_converter.md) and [Easy Lists](easy_lists.md).

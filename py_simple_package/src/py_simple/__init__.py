from .easy_file_manager import (
    make_blank_file, is_file_there, add_a_line, read_file_to_list,
    remove_file, rename_file, list_files, copy_file,
)
from .easy_date_formatter import (
    get_pretty_date, get_past_pretty_date, get_future_pretty_date,
    dd_mm_yyyy, past_dd_mm_yyyy, future_dd_mm_yyyy,
    mm_dd_yyyy, past_mm_dd_yyyy, future_mm_dd_yyyy,
    slash_dd_mm_yyyy, past_slash_dd_mm_yyyy, future_slash_dd_mm_yyyy,
    slash_mm_dd_yyyy, past_slash_mm_dd_yyyy, future_slash_mm_dd_yyyy,
    list_available_formats,
)
from .easy_converter import (
    seconds_to_hh_mm_ss, miles_to_km, km_to_mile, fluid_oz_to_ml,
    ml_to_fluid_oz, celsius_to_fahrenheit, fahrenheit_to_celsius, kg_to_lb,
    lb_to_kg, meters_to_feet, feet_to_meters, cm_to_inches, inches_to_cm,
    sq_feet_to_sq_meters, sq_meters_to_sq_feet
)
from .easy_numbers import (
    is_even, is_odd, is_evenly_divisible, is_negative, is_positive,
    average, is_prime, percentage_of
)
from .easy_validator import (
    is_valid_email, is_valid_username, is_valid_zipcode, is_valid_url,
    is_password_secure,
)
from .easy_web import (
    get_page_content, is_page_up, get_link_list, get_page_title, count_links,
    print_allowed_tags, count_tags, get_tag_list,
)
from .easy_strings import (
    is_palindrome, remove_extra_spaces, to_kebab_case, to_snake_case,
)

"""
py_simple's public API — re-exports the functions from each easy_* module.
"""

from .easy_ai import (
    ask_ai,
    get_model,
    summarize_text,
    translate_text,
)
from .easy_archive import (
    add_to_zip,
    is_zip_file,
    list_zip_contents,
    unzip_file,
    zip_files,
    zip_folder,
)
from .easy_async import (
    run_at_the_same_time_no_params,
    run_at_the_same_time_with_params,
)
from .easy_colors import (
    contrast_ratio,
    hex_to_rgb,
    hex_to_rgba,
    hsl_to_rgb,
    is_light_color,
    is_valid_hex,
    random_hex_color,
    rgb_to_hex,
    rgb_to_hsl,
)
from .easy_config import (
    gh_workflow_config,
)
from .easy_converter import (
    celsius_to_fahrenheit,
    cm_to_inches,
    fahrenheit_to_celsius,
    feet_to_meters,
    fluid_oz_to_ml,
    hh_mm_ss_to_seconds,
    inches_to_cm,
    kg_to_lb,
    km_to_mile,
    kph_to_mph,
    lb_to_kg,
    meters_to_feet,
    miles_to_km,
    ml_to_fluid_oz,
    mph_to_kph,
    seconds_to_hh_mm_ss,
    sq_feet_to_sq_meters,
    sq_meters_to_sq_feet,
)
from .easy_csv import (
    filter_csv_rows,
    get_csv_columns,
    read_csv_to_list,
    write_csv_from_list,
)
from .easy_data_visualization import (
    plot_data,
)
from .easy_date_formatter import (
    dd_mm_yyyy,
    future_dd_mm_yyyy,
    future_mm_dd_yyyy,
    future_slash_dd_mm_yyyy,
    future_slash_mm_dd_yyyy,
    get_future_pretty_date,
    get_past_pretty_date,
    get_pretty_date,
    list_available_formats,
    mm_dd_yyyy,
    past_dd_mm_yyyy,
    past_mm_dd_yyyy,
    past_slash_dd_mm_yyyy,
    past_slash_mm_dd_yyyy,
    slash_dd_mm_yyyy,
    slash_mm_dd_yyyy,
)
from .easy_dict import (
    count_values,
    find_keys,
    get_nested_value,
    invert_dict,
    lists_to_dict,
    merge_dicts,
    most_common_value,
    rename_key,
    sort_dict_by_key,
    sort_dict_by_value,
)
from .easy_file_manager import (
    add_a_line,
    copy_file,
    is_file_there,
    list_files,
    make_blank_file,
    read_file_to_list,
    remove_file,
    rename_file,
)
from .easy_flow import (
    retry,
    run_py_file,
    run_py_file_safe,
    time_function_call,
    time_it,
)
from .easy_game import (
    basic_game_setup,
    check_if_quit,
    get_mouse_position,
    is_left_mouse_button_clicked,
    is_middle_mouse_button_clicked,
    is_right_mouse_button_clicked,
)
from .easy_generator import (
    generate_api_key,
    generate_otp,
    generate_password,
    generate_qr_code,
    generate_slug,
    generate_uuid,
)
from .easy_images import (
    convert_image,
    create_thumbnail,
    get_image_info,
    resize_image,
    rotate_image,
)
from .easy_json import (
    flatten_json,
    get_json_keys,
    is_json_file,
    is_nested_json,
    open_json,
    pretty_json,
    save_json_data,
    update_json,
)
from .easy_lists import (
    alternate_lists,
    chunk_list,
    find_duplicates,
    flatten_list,
    merge_lists,
    most_common_item,
    rotate_list,
    sort_numbers,
    sort_words,
    sum_all,
    unique_items,
)
from .easy_logging import log_function, log_step
from .easy_math import (
    divisors,
    factorial,
    fibonacci,
    get_least_common_multiple,
    is_perfect_square,
    prime_factorization,
    sum_of_digits,
)
from .easy_numbers import (
    average,
    clamp,
    greatest_common_divisor,
    is_even,
    is_evenly_divisible,
    is_negative,
    is_odd,
    is_positive,
    is_prime,
    percentage_of,
    round_to_nearest,
)
from .easy_random import (
    flip_coin,
    pick_random_item,
    pick_random_items,
    random_int,
    roll_dice,
    shuffle_list,
)
from .easy_regex import (
    extract_emails,
    extract_hex_colors,
    extract_number_sequences,
    extract_numbers,
    extract_urls,
)
from .easy_sql import (
    EasySqlError,
    conditional_run_select,
    delete_all_from_table,
    open_db,
    run_delete,
    run_insert,
    run_select,
    run_update,
)
from .easy_stats import (
    data_range,
    interquartile_range,
    median,
    mode,
    percentile,
    standard_deviation,
    variance,
    z_score,
)
from .easy_strings import (
    count_words,
    is_alphanumeric,
    is_palindrome,
    remove_extra_spaces,
    to_kebab_case,
    to_snake_case,
)
from .easy_text import (
    capitalize_title,
    count_digits,
    count_letters,
    extract_hashtags,
    mask_part,
    pluralize,
    remove_punctuation,
    reverse_words,
    truncate,
    word_frequency,
)
from .easy_validator import (
    is_password_secure,
    is_valid_creditcard,
    is_valid_email,
    is_valid_phone_number,
    is_valid_url,
    is_valid_username,
    is_valid_zipcode,
)
from .easy_web import (
    count_links,
    count_tags,
    get_all_headers,
    get_link_list,
    get_meta_description,
    get_page_content,
    get_page_title,
    get_tag_list,
    is_page_up,
    print_allowed_tags,
)

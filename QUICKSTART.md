<div align="center">

🏠[README](README.md) · 📦[Modules](MODULES.md) · 🆘[Support](SUPPORT.md) · 🚀[Contributing](CONTRIBUTING.md) · 🌟[Contributors](CONTRIBUTORS.md) · 📜[Changelog](CHANGELOG.md) · 🔒[Security](SECURITY.md) · 🌱[Code of Conduct](CODE_OF_CONDUCT.md) · ⚖️[License](LICENSE.md)

</div>

# Quickstart
 
Get up and running with `py-simple-wrap` in under a minute.
 
## Installation
 
```bash
pip install py-simple-wrap
```
 
> **Note:** The PyPI package is named `py-simple-wrap` (the name `py-simple` was already taken), but you still import it as `py_simple` in your code.
 
## Basic Usage
 
Every function is available directly from the top-level package — no need to dig into submodules:
 
```python
from py_simple import make_blank_file, miles_to_km, is_valid_email
 
# Create a new file in one line
make_blank_file("notes.txt")
 
# Convert units without memorizing formulas
distance_km = miles_to_km(26.2)
print(distance_km)  # 42.16...
 
# Validate common input formats
print(is_valid_email("hello@example.com"))  # True
```
 
## A Taste of Each Module
 
### 📂 File handling — `easy_file_manager`
 
```python
from py_simple import make_blank_file, add_a_line, read_file_to_list
 
make_blank_file("todo.txt")
add_a_line("todo.txt", "Buy groceries")
print(read_file_to_list("todo.txt"))
```
 
### 🕰️ Dates — `easy_date_formatter`
 
```python
from py_simple import get_pretty_date, dd_mm_yyyy

print(get_pretty_date())  # e.g. "July 31, 2026"
print(dd_mm_yyyy())  # e.g. "31-07-2026"
```
 
### 🔄 Unit conversion — `easy_converter`
 
```python
from py_simple import celsius_to_fahrenheit, kg_to_lb

print(celsius_to_fahrenheit(20))  # 68.0
print(kg_to_lb(70))  # 154.32...
```
 
### 🔢 Numbers — `easy_numbers`
 
```python
from py_simple import is_prime, average

print(is_prime(17))  # True
print(average([4, 8, 15, 16, 23, 42]))
```
 
### ✅ Validation — `easy_validator`
 
```python
from py_simple import is_password_secure, is_valid_url

print(is_password_secure("hunter2"))  # False
print(is_valid_url("https://example.com"))  # True
```
 
### 🌐 Web — `easy_web`
 
```python
from py_simple import is_page_up, get_page_content
 
print(is_page_up("https://python.org"))  # True
```
 
### 🔤 Strings — `easy_strings`
 
```python
from py_simple import to_snake_case, is_palindrome

print(to_snake_case("Hello World"))  # "hello_world"
print(is_palindrome("racecar"))  # True
```
 
## Next Steps
 
- Browse the **Reference** section in the sidebar for the complete list of functions in every module.
- See the full [README](docs/readme.md) for the complete list of functions in each module.
- Want to contribute? Check out [CONTRIBUTING.md](docs/how-to/contributing.md).

# Adding a New Module Guide 🚀

Want to introduce a brand-new `easy_<name>.py` module to `py-simple-wrap`? Amazing! This guide walks you through the exact steps to create a new module from scratch while keeping it consistent with the project's "Simple" philosophy.

---

## The "Simple" Checklist for a New Module

Before writing any code, make sure your proposed module answers "yes" to these three questions:
1. **Does this wrap a complex Python task into plain English?** (e.g., turning raw regex or random module boilerplate into a one-liner).
2. **Is it beginner-friendly?** 
3. **Does it rely primarily on the standard library where possible?** (If it needs external packages like `pygame` or `matplotlib`, ensure they are handled gracefully via optional extras).

---

## Step-by-Step Implementation

### 1. Create your module file
Place your new Python file inside the source directory:
`py_simple_package/src/py_simple/easy_<name>.py`

### 2. Add the Module-Level Docstring
Every module starts with a short docstring explaining what it wraps and why:
```python
"""
easy_<name> is meant to simplify <what it does>.
Built on top of the <stdlib module> module — no more <the pain point>.
"""
```

### 3. Write Your Helper Functions
- Use descriptive, plain-English names (e.g., `generate_username` instead of `gen_u`).
- Follow the [Docstring Template](docstring_template.md) for every public function (including Args, Returns, and the `=== "The Py_simple Way"` vs `=== "The Traditional Way"` code tabs).
- If your module fails on invalid input, follow the [Custom Exception Template](error_template.md) to raise a clean custom error.

### 4. Export Your Public Functions
Make sure your new functions are accessible from the main package import per the [Public API Export Template](public_api_template.md).

### 5. Add Automated Tests
Create a test file in `tests/test_<name>.py` using `pytest` to cover your new helpers thoroughly. Follow the [Module Tests Template](tests_template.md).

### 6. Write a Tutorial Page
Add a Markdown tutorial page under `docs/tutorial/easy_<name>.md` demonstrating 2–3 functions used together in a realistic mini-example. Follow the [Tutorial Template](tutorial_template.md).

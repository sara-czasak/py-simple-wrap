<div align="center">

🏠[README](README.md) · ⚡[Quickstart](QUICKSTART.md) · 📦[Modules](MODULES.md) · 🆘[Support](SUPPORT.md) · 🌟[Contributors](CONTRIBUTORS.md) · 📜[Changelog](CHANGELOG.md) · 🔒[Security](SECURITY.md) · 🌱[Code of Conduct](CODE_OF_CONDUCT.md) · ⚖️[License](LICENSE.md)

</div>

# Contributing to py-simple-wrap 🚀

First of all, thank you for being here! I created `py-simple-wrap` to help others on their learning journey, and I'm excited to have you join me.

**I struggle with anxiety myself, so I totally understand if you're feeling nervous about contributing. Please don't be!** The absolute worst thing that could happen is that I might ask for a few changes before merging your code. This is a safe space to learn, make mistakes, and grow together.

📚 New here? The [Contributor Hub](https://sara-czasak.github.io/py-simple-wrap/docs/contributor-hub/docstring_template/)
has copy-paste templates for docstrings and tutorial pages, so you're not
guessing at formatting on your first PR.


## ⭐ Enjoying the project?

If py-simple-wrap has been useful, or you just like what it's doing, a star means a lot — it helps other beginners discover the project and keeps me motivated to keep building it. It takes two seconds and costs nothing. 🙏

## The "Simple" Philosophy

Before submitting a new feature, ask yourself: **"Does this make a complex task easier for a beginner?"** My goal is to keep things intuitive and easy to read.

## 🛠️ Step-by-Step Guide for Beginners

If you've never contributed to an open-source project before, here is exactly how to do it:

1. **Fork the Project**: Click the "Fork" button at the top right of this GitHub page. This creates your own copy of the project.
2. **Get the Clone Link**:
   - On **your fork's** GitHub page, click the green **<> Code** button.
   - Make sure the **HTTPS** tab is selected.
   - Click the little "copy" icon (two overlapping squares) next to the URL to copy it to your clipboard.
3. **Clone Your Fork**: Open your terminal, type `git clone `, and then paste the link you just copied:

   ```
   git clone https://github.com/YOUR_USERNAME/py-simple-wrap.git
   ```

4. **Create a Branch**: It's best to do your work on a new branch:

   ```bash
   git checkout -b my-new-feature
   ```

5. **Set up the Environment**: We recommend using `uv` for lightning-fast dependency management, but standard `pip` works too!
   - **Using uv (Recommended)**:
     - Install `uv` if you haven't already: [Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
     - Sync the project dependencies:
       ```bash
       uv sync --all-extras --dev
       ```
     - Run the tests to make sure everything works:
       ```bash
       uv run pytest
       ```
   - **Using pip**:
     - Create a virtual environment and install the package with testing and documentation dependencies:
       ```bash
       python -m venv .venv
       # Activate the virtual environment
       # Windows: .venv\Scripts\activate
       # macOS/Linux: source .venv/bin/activate
       pip install -e .[test,docs]
       ```
     - Run the tests:
       ```bash
       pytest
       ```

6. **Preview the Docs Locally**: If you are modifying documentation or adding new tutorials, you can preview the site locally using MkDocs.
   - Using uv:
     ```bash
     uv run mkdocs serve
     ```
   - Using pip:
     ```bash
     mkdocs serve
     ```
   Open `http://127.0.0.1:8000` in your browser to view the site.

7. **Write Your Code**: Add your awesome new function or fix that bug! If you're
not sure how to format a docstring or write a tutorial page, check the
[Contributor Hub](https://sara-czasak.github.io/py-simple-wrap/docs/contributor-hub/docstring_template/)
on the docs site — it has copy-paste templates for both, built from this
project's actual conventions.


8. **Commit Your Changes**: Save your progress with a helpful message:

   ```bash
   git add .
   git commit -m "Added a new helper for list cleaning"
   ```

9. **Push to GitHub**: Send your changes back to your fork:

   ```bash
   git push origin my-new-feature
   ```

10. **Open a Pull Request**: Go to the original `py-simple-wrap` repository on GitHub, and you'll see a button that says "Compare & pull request." Click it and tell me a bit about what you did!

## 💡 What should I contribute?

- **Report Bugs**: If something isn't working, open an "Issue" and let me know.
- **New Ideas**: Want to add a "Simple" module for math, strings, or colors? Open an Issue and we can brainstorm it together!
- **Documentation**: Spot a typo in this README? I'd love for you to fix it!

## Coding Style

I try to keep the code "Clean" and "Explicit."

- Use descriptive function names (like `is_file_there` instead of `check`).
- Always include Docstrings with an example — see the
[Docstring Template](https://sara-czasak.github.io/py-simple-wrap/docs/contributor-hub/docstring_template/)
in the Contributor Hub for the exact shape we use.
- Use existing helper functions (like `is_valid_extension`) to keep things consistent.

Thank you for being brave enough to try! I can't wait to see what you build. 🌈✨

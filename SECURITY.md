 <div align="center">

🏠[README](README.md) · ⚡[Quickstart](QUICKSTART.md) · 📦[Modules](MODULES.md) · 🆘[Support](SUPPORT.md) · 🚀[Contributing](CONTRIBUTING.md) · 🌟[Contributors](CONTRIBUTORS.md) · 📜[Changelog](CHANGELOG.md) · 🌱[Code of Conduct](CODE_OF_CONDUCT.md) · ⚖️[License](LICENSE.md)

</div>

# Security Policy 🔒

## Supported Versions

`py-simple-wrap` is a young project and hasn't reached a stable `1.0` release yet, so there isn't a long history of versions to maintain in parallel. Only the **latest published release on PyPI** receives security fixes.

| Version | Supported |
|---|---|
| Latest release on [PyPI](https://pypi.org/project/py-simple-wrap/#history) | ✅ |
| Any older release | ❌ |

If you're on an older version, please upgrade to the latest release before reporting — there's a good chance it's already fixed.

## Supported Python Versions

Starting with **v0.9.0**, `py-simple-wrap` requires **Python 3.11 or newer**.

**Python 3.10 support has been discontinued due to security vulnerabilities affecting Pillow**, a dependency used by the library's image utilities.

The project currently supports:

- Python 3.11
- Python 3.12
- Python 3.13
- Python 3.14

Users running Python 3.10 should upgrade to Python 3.11 or newer to receive future updates and security fixes.

## Reporting a Vulnerability

Please **do not open a public GitHub Issue** for security vulnerabilities — that could expose the problem to others before it's fixed.

Instead, report it privately to the maintainer, **[@sara-czasak](https://github.com/sara-czasak)**, using [GitHub's private vulnerability reporting](https://github.com/sara-czasak/py-simple-wrap/security/advisories/new) on this repo (Security tab → "Report a vulnerability").

When reporting, please include:

- A description of the vulnerability and its potential impact
- Steps to reproduce it (a minimal code snippet is ideal)
- The version of `py-simple-wrap` you're using
- Your Python version, if relevant

**What to expect:**

- I'll acknowledge your report within **3–5 days**.
- I'll keep you updated on progress at least **once a week** while it's being investigated.
- If the vulnerability is confirmed, I'll work on a fix and aim to release a patched version as quickly as possible, then credit you in the release notes (unless you'd rather stay anonymous).
- If it's declined (e.g. not reproducible, or determined not to be a security issue), I'll explain why.

Since this is a solo-maintained, beginner-focused project, response times may occasionally be a little slower than a large project's SLA — thank you in advance for your patience, and for helping keep `Py_simple` safe for the people learning from it. 🌱
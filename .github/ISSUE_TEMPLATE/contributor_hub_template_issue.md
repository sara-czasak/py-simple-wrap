---
name: 🧭 Add a new guide to the Contributor Hub
about: Write a new template/guide for something not yet covered in the Contributor Hub
title: 🧭 Add a new guide to the Contributor Hub
labels: documentation, good first issue, help wanted, good-first-issue
milestone: v1.0.0
---
The [Contributor Hub](https://sara-czasak.github.io/py-simple-wrap/docs/contributor-hub/) exists so nobody has to guess how this project formats things — docstrings, tutorials, exceptions, and so on each have a fill-in-the-blanks template.

This issue is an invitation to write a **new guide** for something that doesn't have one yet — something you had to figure out by digging through the codebase or asking, that a future contributor shouldn't have to.

### A few guidelines

- **Pick something not already covered.** Check the existing hub pages first: [Docstring Template](https://sara-czasak.github.io/py-simple-wrap/docs/contributor-hub/docstring_template/), [Tutorial Template](https://sara-czasak.github.io/py-simple-wrap/docs/contributor-hub/tutorial_template/), [Custom Exception Template](https://sara-czasak.github.io/py-simple-wrap/docs/contributor-hub/error_template/).
- **Keep it beginner-friendly.** Same audience as the rest of py-simple-wrap — someone making their first open-source contribution, not an experienced maintainer.
- **Fill-in-the-blanks beats prose.** The existing guides work because they give a copy-paste starting point first, with the "why" as optional reading after.
- **Match the tone and structure** of the existing pages in [`docs/contributor-hub/`](https://github.com/sara-czasak/py-simple-wrap/tree/main/docs/contributor-hub).

Once it's written, add it under [`docs/contributor-hub/`](https://github.com/sara-czasak/py-simple-wrap/tree/main/docs/contributor-hub), link it from [`docs/contributor-hub/index.md`](https://github.com/sara-czasak/py-simple-wrap/blob/main/docs/contributor-hub/index.md), and add it to [`mkdocs.yml`](https://github.com/sara-czasak/py-simple-wrap/blob/main/mkdocs.yml) under `Contributor Hub:`, following the same format as the existing entries.

Please read [CONTRIBUTING.md](https://github.com/sara-czasak/py-simple-wrap/blob/main/CONTRIBUTING.md) before you start!
Not sure what's missing? Open a PR anyway or start a discussion here — happy to talk it through.

**Links:**
- Contributor Hub: [`docs/contributor-hub/`](https://sara-czasak.github.io/py-simple-wrap/docs/contributor-hub/)
- Where it goes: [`docs/contributor-hub/`](https://github.com/sara-czasak/py-simple-wrap/tree/main/docs/contributor-hub)
- Hub index to update: [`docs/contributor-hub/index.md`](https://github.com/sara-czasak/py-simple-wrap/blob/main/docs/contributor-hub/index.md)
- Contributing guide: [`CONTRIBUTING.md`](https://github.com/sara-czasak/py-simple-wrap/blob/main/CONTRIBUTING.md)

# Contributor Hub

New here, or making your first contribution to an open-source project ever? You're in the right place. Nobody expects you to already know how this project formats things — that's what this page is for.

Pick whatever's stressing you out below, and go straight to it. You don't need to read all of it, and you don't need to read it in order.

## What do you need help with?

**📝 "I need to write a docstring and I don't know what that even means."**
Totally normal. The [Docstring Template](docstring_template.md) has a copy-paste block — just fill in the blanks. It also explains *why* the format looks the way it does, in case you're curious, but you don't have to read that part to use it.

**📖 "I added a new module and need to write a tutorial page, but I've never written docs before."**
The [Tutorial Template](tutorial_template.md) walks through the exact structure every tutorial page in this project uses, with a real example to copy from. You're not writing from a blank page.

**🧩 "The issue asks for a project that uses two modules, not one module page."**
The [Project-Based Tutorial Template](project_tutorial_template.md) is the fill-in-the-blanks page for that build, plus where it goes in `mkdocs.yml`.

**🚨 "My function needs to raise an error, and I don't know how this project wants errors to look."**
The [Custom Exception Template](error_template.md) has a fill-in-the-blanks class definition, plus a worked example showing both raising and catching it. Errors sound intimidating, but the pattern here is always the same one — once you've seen it once, you'll recognize it everywhere in this codebase.

**🏗️ "I want to add a brand-new module from scratch, from file creation to tests."**
The [Adding a New Module Guide](new_module_template.md) walks through the complete checklist, file locations, docstring requirements, and testing steps.

**✏️ "The issue asks me to add one function to a module that already exists."**
The [Adding a Function to an Existing Module](expand_module_template.md) guide lists the files to touch, where the tests go, and how to export the helper without creating a new module.

**📦 "My helper works in its module, but I cannot import it from py_simple."**
The [Public API Export Template](public_api_template.md) shows where to expose a helper, how to check both import paths, and how to avoid name collisions.

**🌐 "My test calls a website. How do I test it without going online?"**
The [Network Test Template](network_tests_template.md) gives you a working example with fake responses and request failures, then shows which parts to change for your own helper.

**🧹 "A pre-commit check failed, or changed my files. What do I do next?"**
The [Pre-commit Guide](pre_commit_template.md) shows how to run the repository's hooks, review their fixes, and stage and check your files again.

**🔀 "I wrote my changes, but what are the exact steps to test, commit, and open a PR?"**
The [Pull Request Workflow Guide](pr_workflow_template.md) breaks down the complete lifecycle: branch naming, running local pytest and ruff checks, formatting commit messages, opening the pull request, and addressing review feedback.

**🎲 "My helper uses randomness. How can its tests pass reliably?"**
The [Testing Random Helpers](random_tests_template.md) guide shows controlled draws, boundary cases, and shuffle checks that accept every valid ordering.

## Still stuck, or something's not covered here?

That's okay too. Open an issue, or mention it in your pull request, and it'll get sorted out together — see [CONTRIBUTING.md](https://github.com/sara-czasak/py-simple-wrap/blob/main/CONTRIBUTING.md) for how to reach out. Nobody's expected to figure this out alone.

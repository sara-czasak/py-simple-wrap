# Project-Based Tutorial Template

A **module tutorial** explains one `easy_*` helper set. A **project-based
tutorial** combines **at least two modules** into a small build someone
would actually want to try. This page is the fill-in-the-blanks path for
that second kind. For a single-module page, use the
[Tutorial Template](tutorial_template.md).

## Copy this page

Save it as `docs/tutorial/<short-name>-project.md`. Replace the
placeholders, then run the code and paste the real output.

````markdown
# Build a <Project Name> with Easy <A> and Easy <B>

Combine **Easy <A>** and **Easy <B>** to <one-sentence job>.

## A small real-world example

<Two or three sentences. Say who it is for, and whether the sample
writes a temporary file.>

Install the package with `python -m pip install py-simple-wrap`, then run:

```python
from py_simple import helper_a, helper_b

...
```

Example output:

```text
<paste what the script actually printed>
```

## What happened?

<One short paragraph per helper, in the order the script calls them.>

## Try it yourself

<One small tweak: another input, a second file, a stricter check.>

## Why use these helpers?

<What the standard-library version would make you juggle, in one
paragraph. Link the two module tutorials at the end.>
````

## Where it goes

Add **one** line under `Tutorial: > Project-Based Tutorials:` in
[`mkdocs.yml`](../../mkdocs.yml), after the last existing project, using
the same indent as the others:

```yaml
          - <Project Name>: tutorial/<short-name>-project.md
```

Do not add a Reference page. Do not add a README badge. Those are for
new modules, not for a project write-up.

## Rules of thumb

- **Two modules minimum.** `easy_csv` plus `easy_url` is a project.
  Only `easy_csv` is a module tutorial.
- **Keep the result fun and small.** A club badge, a link shelf, a
  lunch picker — not a walkthrough of every function in both modules.
- **Run the sample.** The output block must match what Python prints
  on a current checkout.
- **Prefer a `TemporaryDirectory`** when the script writes a file, so
  readers can re-run it without cluttering their disk.
- **Look at the existing project list first**, so you do not repeat
  Class Link Shelf, Palette Journal, or Message Detective with a new
  title.

## A real example

[Class Link Shelf](../tutorial/class-link-shelf-project.md) strips a
tracking parameter with Easy URL, then saves the cleaned rows with Easy
CSV. That is the shape: one job, two helpers, real output, a "try it
yourself" tweak.

<div align="center">

🏠[README](README.md) · ⚡[Quickstart](QUICKSTART.md) · 📦[Modules](MODULES.md) · 🆘[Support](SUPPORT.md) · 🚀[Contributing](CONTRIBUTING.md) · 🌟[Contributors](CONTRIBUTORS.md) · 🔒[Security](SECURITY.md) · 🌱[Code of Conduct](CODE_OF_CONDUCT.md) · ⚖️[License](LICENSE.md)

</div>

# Changelog
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.7.0] - 2026-09-25

### Added
- Added a circular logo to the README header ([@sara-czasak](https://github.com/sara-czasak))

### Changed
- **Breaking:** `pip install py-simple-wrap` now installs a lightweight core instead of every dependency for every module. Heavy per-module dependencies (`matplotlib`, `pygame-ce`, `Pillow`, `qrcode`, `GitPython`, `python-benedict`, `pydantic`, `langchain-core`) moved out of the default install into per-module extras (`ai`, `game`, `viz`, `images`, `web`, `config`, `json`); `pip install py-simple-wrap[all]` restores the previous batteries-included install. `import py_simple` no longer requires any of these packages to be installed — each heavy import is now deferred to the specific function that uses it ([@sara-czasak](https://github.com/sara-czasak))

### Fixed
- Fixed the docs site rendering the README's title, badges, "Modules at a glance" table, and collaborators section as raw unprocessed text instead of real HTML — `mkdocs.yml` was missing the `md_in_html` extension needed to parse Markdown nested inside `<div>` blocks ([@sara-czasak](https://github.com/sara-czasak))
- Removed the redundant GitHub-style nav bar from docs-site pages (README, Quickstart, Contributing, Contributors, License) via `include-markdown` start markers, since the site already has its own navigation ([@sara-czasak](https://github.com/sara-czasak))

## [0.6.1] - 2026-09-17
### Fixed
- Cleaned up a stray leftover table row in the README's module grid ([@sara-czasak](https://github.com/sara-czasak))
- Fixed the "😰 → 😎 See the difference" heading rendering as literal `## ` text instead of a heading — it immediately followed a `<br>` HTML tag with no blank line between them, which breaks Markdown heading parsing on GitHub ([@sara-czasak](https://github.com/sara-czasak))

## [0.6.0] - 2026-09-17
### Added
- Migrated the project from Poetry/pip to `uv` for dependency management, with `astral-sh/setup-uv` wired into CI and both `uv sync`/`uv run` and a plain `pip install -e .[test,docs]` path documented in `CONTRIBUTING.md`, including local MkDocs preview instructions ([@Yuvrajup](https://github.com/Yuvrajup))
- Added the `easy_logging` module (`log_step`, `log_function`) to the public API, plus `clear_log_file` for emptying a log file's contents ([@sara-czasak](https://github.com/sara-czasak), [@dave123981](https://github.com/dave123981))
- Added `mean` and `correlation_coefficient` (Pearson) to `easy_stats` ([@Voyagerroc-Lab](https://github.com/Voyagerroc-Lab), [@9anna-na](https://github.com/9anna-na))
- Added `random_bool` to `easy_random`, along with a simple `generate_simple_password` helper — named to avoid colliding with the existing, cryptographically-secure `easy_generator.generate_password` ([@ege-arhan](https://github.com/ege-arhan), [@NANDINI-7777](https://github.com/NANDINI-7777))
- Added `update_screen` and `fill_background` to `easy_game`'s public API. `is_key_pressed` was also added to the module but isn't exported yet — it doesn't have test coverage, so it's reachable via `from py_simple.easy_game import is_key_pressed` directly for now ([@Utkarsh3725](https://github.com/Utkarsh3725), [@VidyavathiGK](https://github.com/VidyavathiGK))
- Added `run_with_delay` and `run_with_fallback` to `easy_flow` ([@VidyavathiGK](https://github.com/VidyavathiGK))
- Added 11 new functions to `easy_math` (`is_armstrong_number`, `is_triangular_number`, `is_harshad_number`, `digit_count`, `reverse_digits`, `is_abundant_number`, `distance_between_points`, `midpoint`, `sum_of_squares`, `calculate_simple_interest`, `collatz_sequence`) ([@Yuktheshwarbhat](https://github.com/Yuktheshwarbhat))
- Added `extract_mentions` and `clean_extra_whitespace` to `easy_regex`'s public API. `extract_hashtags` was also added to the module, but isn't exported — it collides with the existing `easy_text.extract_hashtags`, so it stays reachable via `from py_simple.easy_regex import extract_hashtags` directly ([@Yuktheshwarbhat](https://github.com/Yuktheshwarbhat))
- Added a "Share what you build" section and a `#py-simple-wrap` mention to the README ([@sara-czasak](https://github.com/sara-czasak))
- Added a "Smart Web Contact Scraper" project-based tutorial ([@Yuktheshwarbhat](https://github.com/Yuktheshwarbhat))

### Fixed
- Fixed the `away_status.yml` workflow, which was missing a checkout step and failing on every run ([@sara-czasak](https://github.com/sara-czasak))
- Fixed a Codecov coverage gap in `easy_regex` ([@gaoharimran29-glitch](https://github.com/gaoharimran29-glitch))
- Brought `easy_ai` to full test coverage by adding tests for `EasyAgent` and the remaining `get_model` provider branches ([@Yuvrajup](https://github.com/Yuvrajup))
- Removed a duplicate `tests/test_easy_random.py`, consolidating its unique coverage into the existing `tests/test_random.py` ([@HarshRajSinghania](https://github.com/HarshRajSinghania))

## [0.5.0] - 2026-09-08
### Added
- `easy_ai`'s `get_model`, `ask_ai`, `summarize_text`, and `translate_text` are now part of the public API (`from py_simple import ...`), for connecting to OpenAI, Ollama, Anthropic, Google, and Mistral chat models without hand-rolling each provider's SDK setup, with full test coverage, a reference page, and a tutorial. The `EasyAgent` class is still work-in-progress and not exported ([@VidyavathiGK](https://github.com/VidyavathiGK), [@Larslllllll](https://github.com/Larslllllll), [@Ctrl-Yam](https://github.com/Ctrl-Yam), [@sara-czasak](https://github.com/sara-czasak))
- `easy_sql`'s query/write helpers (`run_insert`, `run_select`, `conditional_run_select`, `run_update`, `run_delete`, `delete_all_from_table`, `EasySqlError`) are now part of the public API — the `ExperimentalWarning` added in 0.4.0 has been removed now that they have full test coverage ([@sara-czasak](https://github.com/sara-czasak), [@AhmadBilalDSA](https://github.com/AhmadBilalDSA))
- Added `get_json_keys` to `easy_json`, for pulling the top-level keys out of a dict/JSON structure ([@Saturday-boyi](https://github.com/Saturday-boyi))
- Added `extract_hex_colors` to `easy_regex` and `pick_random_items` to `easy_random`, for selecting multiple random items at once ([@be-student](https://github.com/be-student))
- Added `z_score` and `interquartile_range` to `easy_stats` ([@Steve99bs](https://github.com/Steve99bs))
- Added `create_thumbnail` to `easy_images` ([@be-student](https://github.com/be-student))
- Added `generate_slug` to `easy_generator`, for turning a string into a URL-safe slug ([@BirgirSJakobsson](https://github.com/BirgirSJakobsson))
- Added `is_perfect_square` to `easy_math` ([@be-student](https://github.com/be-student))
- Added `is_valid_creditcard`, `is_valid_phone_number`, `is_valid_ipv4`, `is_valid_ipv6`, `is_valid_json`, and `compare_json` to `easy_validator` ([@ohnsh](https://github.com/ohnsh), [@dave123981](https://github.com/dave123981), [@Killbill584](https://github.com/Killbill584), [@Larslllllll](https://github.com/Larslllllll))
- Added `to_title_case` to `easy_strings`, `draw_text` and `fill_background` to `easy_game`, `run_with_timeout` to `easy_async`, and `run_py_string` to `easy_flow` — not yet part of the public API, but reachable via `from py_simple.<module> import ...` directly ([@UroojFatima-052](https://github.com/UroojFatima-052), [@VidyavathiGK](https://github.com/VidyavathiGK))
- Added an "away status" issue template and workflow, an autoassign-on-request workflow for collaborators, and a stale-PR-closing workflow, so contributor-facing automation keeps running while Sara's at work ([@sara-czasak](https://github.com/sara-czasak))

### Changed
- Standardized `easy_sql`'s error handling around `EasySqlError` as part of removing the experimental warnings ([@sara-czasak](https://github.com/sara-czasak))

### Fixed
- Fixed a bug in `easy_strings` ([@sara-czasak](https://github.com/sara-czasak))
- Removed a stray duplicate `src/` directory left over from an earlier package restructure ([@sara-czasak](https://github.com/sara-czasak))

## [0.4.1] - 2026-08-31
### Added
- Added a feedback-survey call to action to the landing page, matching the one already on the README ([@sara-czasak](https://github.com/sara-czasak))
### Fixed
- Fixed the feedback survey link on the README and the feedback issue template ([@sara-czasak](https://github.com/sara-czasak))

## [0.4.0] - 2026-08-31
### Added
- Added `easy_archive` module (`zip_folder`, `zip_files`, `unzip_file`, `list_zip_contents`, `add_to_zip`, `is_zip_file`) for zipping/unzipping without hand-rolling `zipfile` boilerplate, with full test coverage and a tutorial ([@SemTiOne](https://github.com/SemTiOne), [@anisayakmitra-in](https://github.com/anisayakmitra-in))
- Added `easy_random` module (`roll_dice`, `flip_coin`, `pick_random_item`, `shuffle_list`, `random_int`) for common random choices, with full test coverage, a reference page, and a tutorial ([@VidyavathiGK](https://github.com/VidyavathiGK), [@Betelhem-Sefiw](https://github.com/Betelhem-Sefiw), [@SemTiOne](https://github.com/SemTiOne), [@tasodoufu](https://github.com/tasodoufu))
- Added `easy_config` module (`gh_workflow_config`) for scaffolding GitHub Actions workflow files from a template, with full test coverage and docs ([@sara-czasak](https://github.com/sara-czasak), [@anisayakmitra-in](https://github.com/anisayakmitra-in), [@i-am-paradox](https://github.com/i-am-paradox))
- Expanded `easy_sql` with `run_insert`, `run_select`, `conditional_run_select`, `run_delete`, and `delete_all_from_table`, plus an internal SQL-injection guard shared by all of them ([@sara-czasak](https://github.com/sara-czasak), [@VidyavathiGK](https://github.com/VidyavathiGK))
- Added a project-based tutorial combining `easy_random` and `easy_game`, a signup-validation tutorial for `easy_validator`, and tutorials for `easy_regex` and `easy_sql` (travel wishlist) ([@VidyavathiGK](https://github.com/VidyavathiGK), [@anisayakmitra-in](https://github.com/anisayakmitra-in), [@9anna-na](https://github.com/9anna-na))
- Added a module book/landing page linked from the README ([@sara-czasak](https://github.com/sara-czasak))
- Added a feedback issue template with a survey link, and linked it from the README ([@sara-czasak](https://github.com/sara-czasak))
### Changed
- The five new `easy_sql` query/write functions are not yet part of the public API (`from py_simple import ...`) — only `open_db` is exported. They're still reachable via `from py_simple.easy_sql import ...` directly, but each now raises an `ExperimentalWarning` on call and is marked "Experimental" in its docstring, since none of them have test coverage yet ([@sara-czasak](https://github.com/sara-czasak))
- Standardized error handling in `easy_file_manager`: `InvalidExtension` is now `EasyFileManagerError`, and `make_blank_file` now raises `EasyFileManagerError` if the file already exists instead of silently printing and doing nothing (**breaking change** for anyone catching `InvalidExtension` by name) ([@sara-czasak](https://github.com/sara-czasak))
- Standardized error handling in `easy_archive` to match the rest of the package's exception style ([@sara-czasak](https://github.com/sara-czasak))
- Updated `MODULES.md` and the README's module menu to include `easy_archive`, `easy_config`, and `easy_random`
### Fixed
- Fixed a bug in `easy_file_manager` and a matching exception-name mismatch in its tests ([@sara-czasak](https://github.com/sara-czasak))

## [0.3.5] - 2026-08-21
### Added
- Added a tutorial page for `easy_text` ([@gaoharimran29-glitch](https://github.com/gaoharimran29-glitch))
- Added "What happened" and "Why use these helpers" sections to the `easy_lists` tutorial ([@VidyavathiGK](https://github.com/VidyavathiGK))
- Added a Codecov coverage badge to the README and expanded `tests.yml` to report coverage ([@sara-czasak](https://github.com/sara-czasak))
- Added test coverage for `easy_json`, `easy_validator`, `easy_numbers`, `easy_flow`, `easy_csv`, `easy_colors`, `easy_web`, `easy_converter`, and `easy_date_formatter` ([@Osheun](https://github.com/Osheun), [@matteogristina](https://github.com/matteogristina), [@qiaobochi040726-source](https://github.com/qiaobochi040726-source), [@aditya226-sharma](https://github.com/aditya226-sharma))
- Added an `easy_sql` module (SQLite connection helpers via `open_db`) to the public API, with initial tests ([@sara-czasak](https://github.com/sara-czasak), [@VidyavathiGK](https://github.com/VidyavathiGK))
- Added `MODULES.md`, a standalone module-reference page, moving detailed module-by-module content out of the README ([@sara-czasak](https://github.com/sara-czasak))
- Added `.github/workflows/issues.yml`, which automatically opens issues for modules missing tests, test coverage, reference docs, or tutorials ([@sara-czasak](https://github.com/sara-czasak))
- Added `.github/workflows/new_module_issues.yml`, which maintains a running pool of 5 open "want to add a module?" issues on a weekly schedule ([@sara-czasak](https://github.com/sara-czasak))
- Added `.github/workflows/contributors.yml`, which automatically credits first-time contributors in the README and `CONTRIBUTORS.md` via an auto-opened PR ([@sara-czasak](https://github.com/sara-czasak))
### Changed
- Redesigned `README.md`, trimming it substantially and moving detailed module content out to the new `MODULES.md` ([@sara-czasak](https://github.com/sara-czasak))
- Reworked `publish.yml` to trigger automatically when `pyproject.toml`'s version number changes, and to automatically create the matching git tag and GitHub Release after a successful PyPI publish ([@sara-czasak](https://github.com/sara-czasak))
- Standardized test file naming under `tests/` (e.g. `test_dicts.py` → `test_dict.py`, `test_easy_game.py` → `test_game.py`) ([@sara-czasak](https://github.com/sara-czasak))
- Simplified `CONTRIBUTORS.md`'s guild tiles by removing the per-person blurbs, so new entries can be added automatically ([@sara-czasak](https://github.com/sara-czasak))
### Fixed
- Fixed unresolved git merge-conflict markers accidentally committed into `tests/test_date_formatter.py`, which broke test collection for the entire suite on every Python version ([@sara-czasak](https://github.com/sara-czasak))

## [0.3.4] - 2026-08-17
### Added
- Added Easy Generator and Easy Data Visualization sections to the README module menu (both were exported in the public API but missing from the docs) ([@sara-czasak](https://github.com/sara-czasak))
- Added PyPI download-stats badges (day/week/month) to the README, sourced live from pypistats.org ([@sara-czasak](https://github.com/sara-czasak))
### Fixed
- Fixed a stale Contributor Hub badge link and a malformed table in the README's Easy Text section ([@sara-czasak](https://github.com/sara-czasak))
- Fixed a trailing space in a contributor's commit-history link in the README's contributors table ([@sara-czasak](https://github.com/sara-czasak))
- Fixed a stale `Supported Versions` table in `SECURITY.md` that still named a years-old version number; rewritten to reference "latest PyPI release" instead so it never goes stale again ([@sara-czasak](https://github.com/sara-czasak))
- Excluded `dependabot[bot]` from Contributors Quest tracking — it was showing up as a contributor on the leaderboard ([@sara-czasak](https://github.com/sara-czasak))

## [0.3.3] - 2026-08-17
### Added
- Added a Contributor Hub overview page (`docs/contributor-hub/index.md`) that helps beginners find the right template based on what they're stuck on, instead of landing on the first template page by default ([@sara-czasak](https://github.com/sara-czasak))
- Added a Custom Exception Template to the Contributor Hub, covering the codebase's `<Module>Error` pattern with a worked example ([@sara-czasak](https://github.com/sara-czasak))


## [0.3.2] - 2026-08-17
### Added
- Added `.github/dependabot.yml` to automate dependency updates for pip, npm, and GitHub Actions, with a 7-day cooldown on routine updates (security-alert-driven fixes bypass the cooldown) ([@sara-czasak](https://github.com/sara-czasak))
### Changed
- Bumped GitHub Actions in `pages.yml`/`publish.yml`: `actions/checkout` 4→7, `actions/setup-python` 4→7, `actions/upload-artifact` 4→7, `actions/download-artifact` 4→8, `actions/deploy-pages` 4→5 (Dependabot)
- Bumped `typescript` 5.9.3→7.0.2 and `@types/node` 22.20.1→26.2.0 in the Quest generator's `package.json` (Dependabot)
### Fixed
- Fixed a broken `Documentation` project URL in `pyproject.toml` — pointed at a malformed GitHub folder link that 404'd; now points at the live docs site (`https://sara-czasak.github.io/py-simple-wrap/docs/`) ([@sara-czasak](https://github.com/sara-czasak))
 

## [0.3.1] - 2026-08-17
### Added
- Re-included `easy_data_visualization` (`plot_data`) in the public API now that unit tests exist ([@HeaTTap](https://github.com/HeaTTap))
- Added a "Contributor Hub" docs section with copy-paste Docstring and Tutorial templates ([@sara-czasak](https://github.com/sara-czasak))
- Added a standalone landing page at the GitHub Pages root, linking out to Docs, Contributor Hub, and Contributors Quest ([@sara-czasak](https://github.com/sara-czasak))
- Added the `publish.yml` GitHub Actions workflow for manual PyPI releases ([@sara-czasak](https://github.com/sara-czasak))
### Changed
- Moved the docs site from the GitHub Pages root to `/docs/` to make room for the new landing page; updated `site_url` and internal README/CONTRIBUTING links accordingly ([@sara-czasak](https://github.com/sara-czasak))
- Reorganized README badges into two rows (explore vs. project status) and added Home/Contributor Hub/Contributors badges ([@sara-czasak](https://github.com/sara-czasak))
- Added a Contributor Hub callout to CONTRIBUTING.md pointing new contributors at the docstring/tutorial templates ([@sara-czasak](https://github.com/sara-czasak))

## [0.3.0] - 2026-08-16
### Added
- Contributor "quest" gamification system: guilds, badges, XP and achievement tracking ([@sara-czasak](https://github.com/sara-czasak))
- Added tutorials for `easy_validator`, `easy_regex`, `easy_numbers`, `easy_math`, `easy_lists`, `easy_json`, `easy_images`, `easy_stats` ([@Onion0121](https://github.com/Onion0121), [@Venkat4real](https://github.com/Venkat4real), killmeheaven, Boyeong24 — last two not currently listed in `.all-contributorsrc`)
-- Added `easy_numbers2.md`, `easy_math2.md`, `easy_json2.md` tutorial files ([@Onion0121](https://github.com/Onion0121)); renamed to resolve filename conflicts with other contributors' tutorials ([@sara-czasak](https://github.com/sara-czasak))
- Added Python 3.13/3.14 classifiers and CI matrix entries ([@jbsilva](https://github.com/jbsilva))
### Changed
- Replaced `pygame` with `pygame-ce` as the `easy_game` dependency for Python 3.14 wheel support ([@jbsilva](https://github.com/jbsilva))
- Restructured CONTRIBUTORS.md and added a contributor round table ([@sara-czasak](https://github.com/sara-czasak))
- Added new contributors (E4x7k, jbsilva, Venkat4real) to README/CONTRIBUTORS.md ([@sara-czasak](https://github.com/sara-czasak))
- Excluded `easy_data_visualization` (`plot_data`) from the public API and removed the `matplotlib` dependency until unit tests exist for it ([@sara-czasak](https://github.com/sara-czasak))
### Fixed
- Fixed typo in the Easy Json tutorial path in `mkdocs.yml` ([@sara-czasak](https://github.com/sara-czasak))
- Bug-fixing and optimization passes on the contributor-quest scripts/site ([@sara-czasak](https://github.com/sara-czasak))
- Added missing permissions to the pylint/tests CI workflows ([@sara-czasak](https://github.com/sara-czasak))

## [0.2.0] - 2026-08-09
### Added
- Added JSON flattening functions (`is_nested_json`, `flatten_json`) to `easy_json`; tests added ([@sara-czasak](https://github.com/sara-czasak), [@atiqur-rahman-pro](https://github.com/atiqur-rahman-pro))
- Added `easy_regex` module; tests added ([@sara-czasak](https://github.com/sara-czasak), [@Mlandvo](https://github.com/Mlandvo), [@gaoharimran29-glitch](https://github.com/gaoharimran29-glitch))
- Added `easy_lists` (11 helpers) and `easy_text` (10 helpers) modules, with tests and docs ([@ghostfix-pm](https://github.com/ghostfix-pm))
- Added `easy_csv` module with CSV helpers ([@qotique](https://github.com/qotique))
- Added `easy_colors` functions: `random_hex_color`/`is_light_color` ([@smirnov-danil](https://github.com/smirnov-danil)), `rgb_to_hsl`/`hsl_to_rgb` ([@SemTiOne](https://github.com/SemTiOne)), `hex_to_rgba`/`contrast_ratio` ([@gaoharimran29-glitch](https://github.com/gaoharimran29-glitch))
- Added `run_py_file_safe`, `time_it`, and `retry` to `easy_flow` ([@AureSerua](https://github.com/AureSerua)); added tests ([@thomsonl](https://github.com/thomsonl))
- Added `easy_images` module ([@vjymisal0](https://github.com/vjymisal0))
- Started `easy_game` module, added `check_if_quit` and mouse-press detection ([@sara-czasak](https://github.com/sara-czasak))
- Added `easy_dict`, `easy_math`, and `easy_stats` modules ([@SemTiOne](https://github.com/SemTiOne))
- Added `easy_generator` module and 3 new helper functions ([@sara-czasak](https://github.com/sara-czasak))
- Added initial `easy_data_visualization` module and did a modularization pass ([@joaoprbrasil](https://github.com/joaoprbrasil))
- Added tutorials for `easy_flow`, `easy_async`, `easy_colors`, `easy_converter`, `easy_web` ([@Onion0121](https://github.com/Onion0121))
- Added async test scaffolding ([@AashiSrivastava411](https://github.com/AashiSrivastava411))
### Changed
- Renamed `prime_factors` → `prime_factorization` (and its tests) ([@sara-czasak](https://github.com/sara-czasak))
### Fixed
- Multiple bug-fixing passes across `easy_generator` and other modules ([@sara-czasak](https://github.com/sara-czasak))

## [0.1.1] to [0.1.4] - 2026-07-31
Four patch versions published in quick succession on the same day. Historical commit
detail doesn't distinguish which change shipped in which specific patch, so they're
combined into one entry here rather than guessing at a split.
### Added
- Added unit tests for `easy_web` module (closes #15) ([@HeaTTap](https://github.com/HeaTTap))
- Added `get_page_title` and other new functions to `easy_web`, added unit test workflow ([@sara-czasak](https://github.com/sara-czasak))
- Refactored docs, started building the docs page, added GitHub Pages deployment workflow ([@sara-czasak](https://github.com/sara-czasak))
### Fixed
- Docstring/docs improvements and typo fixes across modules ([@sara-czasak](https://github.com/sara-czasak))
- Various bug fixes and mkdocs config fixes ([@sara-czasak](https://github.com/sara-czasak))

## [0.1.0] - 2026-07-30
### Added
- Started and expanded `easy_numbers` module (`is_prime`, `percentage_of`); tests added ([@sara-czasak](https://github.com/sara-czasak), [@jagjitkaur0000](https://github.com/jagjitkaur0000))
- Added fluid oz/ml conversions and other features to `easy_converter`; tests added ([@sara-czasak](https://github.com/sara-czasak), [@averyquinnhq](https://github.com/averyquinnhq))
- Started and expanded `easy_validator` module; tests added ([@sara-czasak](https://github.com/sara-czasak), [@gaoharimran29-glitch](https://github.com/gaoharimran29-glitch))
- Added `easy_strings` module ([@shivams786](https://github.com/shivams786))
- Added speed converters to `easy_converter` (closes #17) ([@sol4nki](https://github.com/sol4nki))
- Started `easy_web` module, added docstrings and request timeout ([@sara-czasak](https://github.com/sara-czasak))
- `pyproject.toml` expansion, comprehensive tests, and new utility functions ([@ghostfix-pm](https://github.com/ghostfix-pm))
- Enhanced Pylint CI workflow, added `.pylintrc` ([@sara-czasak](https://github.com/sara-czasak))
### Fixed
- Fixed a negative-number bug in `easy_numbers`' prime check ([@sara-czasak](https://github.com/sara-czasak))
### Changed
- Various README/CONTRIBUTORS.md updates ([@sara-czasak](https://github.com/sara-czasak))

## [0.0.1] - 2026-07-22
### Added
- Initial project scaffolding: README, LICENSE, CONTRIBUTING.md, `pyproject.toml` ([@sara-czasak](https://github.com/sara-czasak))
- Added `easy_file_manager` functionality: read-to-list, remove file, rename file ([@sara-czasak](https://github.com/sara-czasak))
- Added `easy_date_formatter` module, made helper functions private ([@sara-czasak](https://github.com/sara-czasak))
### Changed
- README formatting passes (headers, readability) ([@sara-czasak](https://github.com/sara-czasak))
- Prepared files for test coverage ([@sara-czasak](https://github.com/sara-czasak))


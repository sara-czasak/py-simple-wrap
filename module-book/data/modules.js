/*
 * The Big Book of Modules — module data.
 *
 * Assigned to a global instead of loaded as JSON on purpose: the book opens
 * straight from the filesystem (file://), where fetch() is blocked.
 *
 * Categories and summaries follow MODULES.md.
 */

window.BOOK_DATA = {
  categories: [
    {
      id: "ai",
      name: "AI",
      icon: "🤖",
      blurb: "Connect to AI models and work with text without the setup boilerplate"
    },
    {
      id: "files-data",
      name: "Files & data",
      icon: "📂",
      blurb: "Reading, writing, and reshaping the stuff on your disk"
    },
    {
      id: "text-validation",
      name: "Text & validation",
      icon: "🔤",
      blurb: "Tidy up words and check that input is what it claims to be"
    },
    {
      id: "numbers-math",
      name: "Numbers & math",
      icon: "🔢",
      blurb: "Calculations and conversions without re-deriving the formulas"
    },
    {
      id: "time-flow",
      name: "Time & control flow",
      icon: "🕰️",
      blurb: "Dates, timing, retries, and doing several things at once"
    },
    {
      id: "web-visuals",
      name: "Web & visuals",
      icon: "🌐",
      blurb: "Pages, pictures, colors, and charts"
    },
    {
      id: "fun-generators",
      name: "Fun & generators",
      icon: "🎲",
      blurb: "Games, randomness, and things conjured out of thin air"
    }
  ],

  modules: [
    /* ---------------------------------------------------------------- */
    /* AI                                                               */
    /* ---------------------------------------------------------------- */
    {
      id: "easy_ai",
      name: "Easy AI",
      icon: "🤖",
      category: "ai",
      summary: "connect to LLM providers without the SDK setup boilerplate",
      useCases: [
        "Connect to a supported AI provider with one helper",
        "Ask a question or start an interactive chat",
        "Summarize, translate, or rewrite text"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_ai/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_ai/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_ai.py" }
      ]
    },
    /* ---------------------------------------------------------------- */
    /* Files & data                                                     */
    /* ---------------------------------------------------------------- */
    {
      id: "easy_file_manager",
      name: "Easy File Manager",
      icon: "📂",
      category: "files-data",
      summary: "file operations without the os boilerplate",
      useCases: [
        "Check whether a file exists before you try to open it",
        "Append a line to a log file without opening it in the wrong mode",
        "List every .txt file in the current folder",
        "Copy, rename, or delete a file in one readable line"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_file_manager/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_file_manager/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_file_manager.py" }
      ]
    },
    {
      id: "easy_json",
      name: "Easy JSON",
      icon: "📄",
      category: "files-data",
      summary: "JSON file handling without the boilerplate",
      useCases: [
        "Load a settings file into a dictionary in one call",
        "Save your data back out without worrying about encoding",
        "Print a messy API response in a shape you can actually read",
        "Flatten a deeply nested JSON file into flat key/value pairs"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_json/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_json/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_json.py" }
      ]
    },
    {
      id: "easy_csv",
      name: "Easy CSV",
      icon: "📑",
      category: "files-data",
      summary: "CSV reading and writing without the csv module boilerplate",
      useCases: [
        "Read a spreadsheet export into a list of rows you can loop over",
        "Find out what column headings a mystery CSV actually has",
        "Keep only the rows where the status column says \"paid\"",
        "Write your results back out to a new CSV file"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_csv/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_csv/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_csv.py" }
      ]
    },
    {
      id: "easy_dict",
      name: "Easy Dict",
      icon: "🔑",
      category: "files-data",
      summary: "dictionary operations without the boilerplate",
      useCases: [
        "Combine default settings with a user's overrides",
        "Reach into a deeply nested response with a path like \"user.address.city\"",
        "Sort a word-count dictionary so the biggest number comes first",
        "Build a lookup table from a list of names and a list of scores"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_dict/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_dict/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_dict.py" }
      ]
    },
    {
      id: "easy_lists",
      name: "Easy Lists",
      icon: "📋",
      category: "files-data",
      summary: "list helpers that keep your code short and readable",
      useCases: [
        "Strip duplicate email addresses out of a signup list",
        "Split a long list of records into batches of 50",
        "Flatten a list of lists into one flat list",
        "Find the item that shows up most often in your data"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_lists/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_lists/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_lists.py" }
      ]
    },
    {
      id: "easy_sql",
      name: "Easy SQL",
      icon: "🗄️",
      category: "files-data",
            summary: "open a SQLite connection and run queries/writes without the boilerplate",
      useCases: [
        "Open a SQLite database and get a connection and cursor in one call"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_sql/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_sql/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_sql.py" }
      ]
    },
    {
      id: "easy_archive",
      name: "Easy Archive",
      icon: "🗜️",
      category: "files-data",
      summary: "zip and unzip files/folders without the zipfile boilerplate",
      useCases: [
        "Back up a whole project folder into one .zip",
        "Peek inside an archive without extracting it",
        "Unpack a downloaded zip into a folder you choose",
        "Bundle just the handful of files you want to email someone"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_archive/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_archive/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_archive.py" }
      ]
    },
    {
      id: "easy_hash",
      name: "Easy Hash",
      icon: "#️⃣",
      category: "files-data",
      summary: "checksums for text and files without the hashlib boilerplate",
      useCases: [
        "Fingerprint a class note so you can tell if it changed",
        "Checksum a downloaded file before you open it",
        "Compare a sentence with a checksum someone sent you"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_hash/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_hash/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_hash.py" }
      ]
    },
    {
      id: "easy_config",
      name: "Easy Config",
      icon: "⚙️",
      category: "files-data",
      summary: "config file templates with guiding comments, so you don't have to look up the syntax",
      useCases: [
        "Drop a starter GitHub Actions workflow into a new repo",
        "Get a commented template instead of hunting for the right YAML keys",
        "Set up automation on a project without copy-pasting from an old one"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_config/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_config/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_config.py" }
      ]
    },

    /* ---------------------------------------------------------------- */
    /* Text & validation                                                */
    /* ---------------------------------------------------------------- */
    {
      id: "easy_strings",
      name: "Easy Strings",
      icon: "🔤",
      category: "text-validation",
      summary: "string operations that read like English",
      useCases: [
        "Clean up the double spaces in text someone pasted in",
        "Turn \"My Report Title\" into a safe file name like my_report_title",
        "Check whether a word reads the same backwards",
        "Count how many words are in a paragraph"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_strings/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_strings/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_strings.py" }
      ]
    },
    {
      id: "easy_text",
      name: "Easy Text",
      icon: "✂️",
      category: "text-validation",
      summary: "text formatting helpers that read like English",
      useCases: [
        "Cut a long description down to a preview snippet",
        "Hide all but the last four digits of a card number",
        "Say \"1 file\" or \"3 files\" without writing an if statement",
        "Pull the hashtags out of a social media post"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_text/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_text/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_text.py" }
      ]
    },
    {
      id: "easy_regex",
      name: "Easy Regex",
      icon: "🔍",
      category: "text-validation",
      summary: "pull common patterns out of text without writing regex",
      useCases: [
        "Grab every email address out of a pasted block of text",
        "Collect the links mentioned in an article",
        "Find the phone numbers hiding in a contact export",
        "Pull the numbers out of a line so you can add them up"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_regex/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_regex/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_regex.py" }
      ]
    },
    {
      id: "easy_validator",
      name: "Easy Validator",
      icon: "✅",
      category: "text-validation",
      summary: "input validation without regex memorization",
      useCases: [
        "Check that a signup email is really an email address before saving it",
        "Make sure a chosen username fits your rules",
        "Confirm a link is a real URL before trying to fetch it",
        "Tell a user their password isn't strong enough yet"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_validator/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_validator/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_validator.py" }
      ]
    },

    /* ---------------------------------------------------------------- */
    /* Numbers & math                                                   */
    /* ---------------------------------------------------------------- */
    {
      id: "easy_numbers",
      name: "Easy Numbers",
      icon: "🔢",
      category: "numbers-math",
      summary: "number checks and calculations without the mental math",
      useCases: [
        "Do something only on every other loop by checking for even numbers",
        "Work out 15% of a bill for a tip",
        "Keep a volume slider between 0 and 100 no matter what gets passed in",
        "Round a price up to the nearest 5"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_numbers/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_numbers/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_numbers.py" }
      ]
    },
    {
      id: "easy_math",
      name: "Easy Math",
      icon: "🧮",
      category: "numbers-math",
      summary: "math helpers without re-deriving the formulas",
      useCases: [
        "Generate the first ten Fibonacci numbers for a homework problem",
        "Break a number down into its prime factors",
        "List every divisor of a number to check if it's tidy",
        "Find the smallest number two schedules both fit into"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_math/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_math/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_math.py" }
      ]
    },
    {
      id: "easy_stats",
      name: "Easy Stats",
      icon: "📊",
      category: "numbers-math",
      summary: "statistics operations without memorizing the formulas",
      useCases: [
        "Find the middle value of a set of test scores",
        "See which answer came up most often in a survey",
        "Measure how spread out your measurements are",
        "Work out what the 90th percentile response time was"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_stats/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_stats/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_stats.py" }
      ]
    },
    {
      id: "easy_converter",
      name: "Easy Converter",
      icon: "🔄",
      category: "numbers-math",
      summary: "unit conversions without memorizing formulas",
      useCases: [
        "Show a running distance in both kilometres and miles",
        "Turn 3725 seconds into a readable 01:02:05",
        "Convert a recipe from Fahrenheit to Celsius",
        "Swap a room's square feet into square metres"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_converter/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_converter/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_converter.py" }
      ]
    },

    /* ---------------------------------------------------------------- */
    /* Time & control flow                                              */
    /* ---------------------------------------------------------------- */
      {
      id: "easy_logging",
      name: "Easy Logging",
      icon: "🪵",
      category: "time-flow",
      summary: "start/success/error logging around code blocks and function calls without repeating try/except",
      useCases: [
        "Log the start, success, or failure of a code block",
        "Add logging around a function with a decorator",
        "Read recent log lines or search for matching messages"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_logging/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_logging/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_logging.py" }
      ]
    },
    {
      id: "easy_date_formatter",
      name: "Easy Date Formatter",
      icon: "🕰️",
      category: "time-flow",
      summary: "readable dates without memorizing strftime codes",
      useCases: [
        "Stamp today's date on a report in a form people can read",
        "Work out what the date was 30 days ago for a report window",
        "Name a file with the date in DD-MM-YYYY order",
        "Show a due date 14 days from now"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_date_formatter/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_date_formatter/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_date_formatter.py" }
      ]
    },
    {
      id: "easy_flow",
      name: "Easy Flow",
      icon: "🔄",
      category: "time-flow",
      summary: "running scripts, timing, and retries without the boilerplate",
      useCases: [
        "Run another Python script from inside your own",
        "Find out which of two functions is actually the slow one",
        "Retry a flaky network call a few times before giving up",
        "Time a function just by adding a decorator above it"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_flow/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_flow/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_flow.py" }
      ]
    },
    {
      id: "easy_async",
      name: "Easy Async",
      icon: "⚡",
      category: "time-flow",
      summary: "run multiple functions at once without touching ThreadPoolExecutor directly",
      useCases: [
        "Download several pages at the same time instead of one after another",
        "Kick off a batch of slow jobs and collect all the results together",
        "Speed up a script that spends most of its time waiting"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_async/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_async/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_async.py" }
      ]
    },

    /* ---------------------------------------------------------------- */
    /* Web & visuals                                                    */
    /* ---------------------------------------------------------------- */
      {
      id: "easy_terminal",
      name: "Easy Terminal",
      icon: "🖥️",
      category: "web-visuals",
      summary: "styled terminal output without memorizing Rich markup strings",
      useCases: [
        "Print terminal messages in different colors",
        "Highlight text with a background color",
        "Combine color and bold styling using chained methods"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_terminal/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_terminal.py" }
      ]
    },
    {
      id: "easy_web",
      name: "Easy Web",
      icon: "🌐",
      category: "web-visuals",
      summary: "web scraping and checks without the requests/BS4 boilerplate",
      useCases: [
        "Check whether a website is up before linking to it",
        "Grab the title of a page you're bookmarking",
        "Collect every link on a page into a list",
        "Read a page's meta description for a link preview"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_web/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_web/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_web.py" }
      ]
    },
    {
      id: "easy_colors",
      name: "Easy Colors",
      icon: "🎨",
      category: "web-visuals",
      summary: "hex/RGB/HSL color conversions without memorizing the formulas",
      useCases: [
        "Turn a hex code from a design file into RGB values",
        "Decide whether to put black or white text on a background",
        "Check two colors have enough contrast to be readable",
        "Pick a random color for a chart series"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_colors/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_colors/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_colors.py" }
      ]
    },
    {
      id: "easy_images",
      name: "Easy Images",
      icon: "🖼️",
      category: "web-visuals",
      summary: "resize, convert, rotate, and inspect images without wrangling Pillow directly",
      useCases: [
        "Shrink a photo down to a thumbnail for a web page",
        "Turn a PNG into a JPG without opening an image editor",
        "Straighten a scan that came out sideways",
        "Find out how big an image is before you upload it"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_images/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_images/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_images.py" }
      ]
    },
    {
      id: "easy_data_visualization",
      name: "Easy Data Visualization",
      icon: "📈",
      category: "web-visuals",
      summary: "auto-picks the right chart type for your data, no matplotlib boilerplate",
      useCases: [
        "Chart a month of sales figures without choosing a chart type first",
        "See the shape of a single list of numbers at a glance",
        "Plot two columns against each other to look for a pattern"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_data_visualization/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_data_visualization/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_data_visualization.py" }
      ]
    },

    /* ---------------------------------------------------------------- */
    /* Fun & generators                                                 */
    /* ---------------------------------------------------------------- */
    {
      id: "easy_game",
      name: "Easy Game",
      icon: "🎮",
      category: "fun-generators",
      summary: "pygame setup without the boilerplate",
      useCases: [
        "Get a game window on screen in one line so you can start building",
        "Close the window cleanly when someone clicks the X",
        "Find out where the mouse is and whether it was clicked"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_game/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_game/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_game.py" }
      ]
    },
    {
      id: "easy_generator",
      name: "Easy Generator",
      icon: "🎲",
      category: "fun-generators",
      summary: "passwords, QR codes, UUIDs, and API keys without the boilerplate",
      useCases: [
        "Make a strong password of the length you want",
        "Turn a link into a QR code image for a poster",
        "Give every record in your data a unique id",
        "Send someone a one-time code to confirm their login"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_generator/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_generator/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_generator.py" }
      ]
    },
    {
      id: "easy_random",
      name: "Easy Random",
      icon: "🔀",
      category: "fun-generators",
      summary: "dice, coin flips, and shuffles without wiring up the random module",
      useCases: [
        "Roll a six-sided die for a board game you're building",
        "Flip a coin to settle a tie between two options",
        "Pick a random winner out of a list of names",
        "Shuffle a deck of cards without changing the original list"
      ],
      links: [
        { label: "Docs", icon: "📘", url: "https://sara-czasak.github.io/py-simple-wrap/docs/reference/easy_random/" },
        { label: "Tutorial", icon: "🎓", url: "https://sara-czasak.github.io/py-simple-wrap/docs/tutorial/easy_random/" },
        { label: "Source", icon: "🐍", url: "https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/easy_random.py" }
      ]
    }
  ]
};

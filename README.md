# Static Site Generator

A Python static site generator that converts Markdown content into HTML pages.

The project supports:

- Markdown paragraphs and headings
- Fenced code blocks
- Blockquotes
- Ordered and unordered lists
- Bold, italic, and inline code
- Links and images
- Nested content directories
- HTML templates with title and content placeholders
- Configurable deployment base paths

## Requirements

- Python 3.10+
- Bash

The project uses only the Python standard library.

## Project Structure

```text
.
├── content/          # Markdown source files
├── static/           # Static assets such as CSS and images
├── docs/             # Generated GitHub Pages output
├── preview/          # Local preview output (ignored by Git)
├── template.html     # HTML page template
├── src/
│   ├── markdown_blocks.py  # Block parsing and block-to-HTML conversion
│   ├── textnode.py         # Inline Markdown parsing and text nodes
│   ├── gencontent.py       # Title extraction and page generation
│   └── main.py             # Build orchestration
├── build.sh            # Build site for GitHub Pages
├── main.sh             # Generate and serve locally
├── test.sh             # Run unit tests
└── README.md
```

## Run Tests

```bash
./test.sh
```

The test suite covers Markdown parsing, HTML node generation, page generation, static asset copying, and recursive page generation.

## Build the Site

To generate the deployment site into `docs/`:

```bash
./build.sh
```

The build script uses `/ssg/` as the deployment base path for the GitHub Pages project site. Generated HTML pages and copied static assets are written to the tracked `docs/` directory.

## Preview Locally

To generate the site into the ignored `preview/` directory and start a local server:

```bash
./main.sh
```

Then open [http://localhost:8888](http://localhost:8888).

The local script uses `/` as the base path and writes to `preview/`, while `build.sh` uses `/ssg/` and writes to `docs/` for deployment. This prevents local previews from overwriting deployment-ready files.

## Adding Content

Add Markdown files under `content/`. Nested directories are mirrored into the selected output directory (`preview/` locally or `docs/` for deployment).

For example:

```text
content/blog/example/index.md
```

generates:

```text
docs/blog/example/index.html
```

Each page should contain an H1 heading because the first H1 is used as the page title:

```markdown
# My Page Title

Page content goes here.
```

## Template Variables

`template.html` supports these placeholders:

```text
{{ Title }}
{{ Content }}
```

`{{ Title }}` is replaced with the first H1 heading, and `{{ Content }}` is replaced with the generated HTML.

## Deployment

The generated `docs/` directory is intentionally committed because it is the deployment source for GitHub Pages.

After changing content or templates:

```bash
./build.sh
git add .
git commit -m "build: regenerate GitHub Pages output"
git push
```

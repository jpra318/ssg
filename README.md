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

To generate the site into `docs/`:

```bash
./build.sh
```

The build script uses `/ssg/` as the deployment base path for the GitHub Pages project site. Generated HTML pages and copied static assets are written to `docs/`.

## Preview Locally

To generate the site and start a local server:

```bash
./main.sh
```

Then open [http://localhost:8888](http://localhost:8888).

The local script uses `/` as the base path, while `build.sh` uses `/ssg/` for deployment under the GitHub Pages project path.

## Adding Content

Add Markdown files under `content/`. Nested directories are mirrored into `docs/`.

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

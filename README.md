# Parse 2 Docs

![PyPI](https://img.shields.io/pypi/v/parse2docs)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/MrCordeiro/parse2docs/actions/workflows/tests.yml/badge.svg)](https://github.com/MrCordeiro/parse2docs/actions/workflows/tests.yml)
[![Linters](https://github.com/MrCordeiro/parse2docs/actions/workflows/linters.yml/badge.svg)](https://github.com/MrCordeiro/parse2docs/actions/workflows/linters.yml)

`parse2docs` is a Python library that allows you to automatically generate usage documentation in Markdown format from Python scripts using the `argparse` module.

## Features

* Scans the Python script for instances of `argparse.ArgumentParser`.
* Generates a Markdown file with usage documentation based on the `ArgumentParser` object.
* The generated documentation includes a table of contents, descriptions of each command line argument, and examples if provided.
* Works with `ArgumentParser` instances declared at the module level or returned by functions.

## Installation

`parse2docs` can be installed via `pip`:

```shell
pip install parse2docs
```

## Usage

There are two ways to use parse2docs, either as a Python module in your script or directly from the command line using the provided command.

### As a Python module

```python
import parse2docs

# Path to the Python script
script_path = 'path_to_your_python_script.py'

# Generate markdown documentation
markdown = parse2docs.generate_md_from_py_script(script_path)

# Save the markdown to a .md file
with open('output.md', 'w') as f:
    f.write(markdown)
```

This will generate a `output.md` file with the usage documentation in Markdown format.

### From the command line

#### Description

The following usage section was generated using `parse2docs` 😉:

```md
## Overall Usage Example

`example.py <file_path>`

## Table of Contents

* [file_path](#file_path)

## Options

### file_path

Path to the Python script file containing the ArgumentParser.

**Type**: `Path`

**Required**: Yes
```

This will print the usage documentation in Markdown format to the console.

## Testing

We use `pytest` for testing. Run the tests with the following command:

```bash
python -m pytest tests/
```

## Contributing

Contributions to `parse2docs` are welcome and awesome! Please submit a pull request or open an issue to discuss potential changes or improvements.

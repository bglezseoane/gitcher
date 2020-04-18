# Installation guide

This software is available for Unix-like systems (Linux and MacOS).

## Homebrew (recommended for MacOS)

You can use Homebrew to install this program via my tap repository:

```sh
brew install bglezseoane/tap/gitcher
```

## Pip (recommended for Linux)

You also can use PYPI to install this program:

```sh
pip install gitcher
```

## Manual

Alternative, clone and go to this repository home directory, and then run:

```sh
python setup.py install
```

## Additional notes

All methods install last Gitcher stable version on your machine. Now you can run it on your shell using:

```sh
gitcher
```

<br>

Read the man of this tool to known more about its use.

**Note about man pages**: if you use `pip` method to install this program, assert that man directories of your Python environment are added to your `MANPATH` to can get this program's man pages with the `man` command. Python might install man pages in default machine level directories.

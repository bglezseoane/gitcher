# gitcher

The git profile switcher. It facilitates the switching between git profiles, importing configuration settings such as name, email and user signatures.

![Screen capture](docs/screen.png?raw=true "Screen capture")


## Purpose

It is possible that you have multiple git configurations. E.g.:

- Work profile

```
Name: Jane Doe
Email: janedoe@work
PGP Key: AAAA1234
```

- Personal profile

```
Name: Jane Doe
Email: janedoe@home
PGP Key: BBBB5678
```

It could be a nuisance to switch between profiles while working on different projects. In addition, it is common to forget what profile you are using when you start commit in a new repository, and rewrite your story can be a bigger nuisance.

This tool aims to facilitate the configuration of the profile to be used in each project, an agile exchange between the different profiles and a way to control the profiles that you are using in your machine.


## What is a gitcher profile?

A profile is a git configuration data set that includes:

- Name.
- Email.
- PGP Key (optional).
- GPG autosigning preference (activate it do that every commit will be signed).

It is identified by a subject tittle like "work" or "university" that have to be unique.


## Saved data

The `~/.cherfile` file contains the saved profiles data.


## To set up

You can use Homebrew to install this program via my tap repository:

```sh
brew install glezseoane/homebrew-tap/gitcher
```

You also can use PyPI to install this program:

```sh
pip install gitcher
```

Alternative, clone and go to this repository home directory, and then run:

```sh
python setup.py install
```

Both methods install last Gitcher stable version on your machine. Now you can run it on your shell using:

```sh
gitcher
```

<br>

Read the man of this tool to known more about its use.

> Note about man pages: if you use `pip` method to install this program, assert that man directories of your Python environment are added to your `MANPATH` to can get this program's man pages with the `man` command. Python might install man pages in default machine level directories.


## Acknowledgments
Santiago Fernández González for an effusive reception of the tool, being the highest tester of Gitcher after its own author.

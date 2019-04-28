# gitcher

The git profile switcher. It facilitates the switching between git profiles, importing configuration settings such as name, email and user signatures.

![Screen capture](docs/screen.png?raw=true "Screen capture")


## Purpose

It is possible that you have multiple git configurations. E.g.:

- Work profile

```
Name: Jane Doe
Email: janedoe@work
GPG Key: AAAA1234
```

- Personal profile

```
Name: Jane Doe
Email: janedoe@home
GPG Key: BBBB5678
```

It could be a nuisance to switch between profiles while working on different projects. In addition, it is common to forget what profile you are using when you start commit in a new repository, and rewrite your story can be a bigger nuisance.

This tool aims to facilitate the configuration of the profile to be used in each project, an agile exchange between the different profiles and a way to control the profiles that you are using in your machine.


## What is a gitcher profile?

A profile is a git configuration data set that includes:

- Name.
- Email.
- GPG Key (optional).
- GPG autosigning preference (activate it do that every commit will be signed).

It is identified by a subject tittle like "work" or "university" that have to be unique.


## Saved data

The `~/.cherfile` file contains the saved profiles data.


## To set up

You can use PyPI to install this program:

```
$ pip install gitcher
```

Alternative, clone and go to this repository home directory, and then run:

```
$ python setup.py install
```

Both methods install last **gitcher** stable version on your machine. Now you can run it on your shell using:

```
$ gitcher
```

Read the man of this tool to known more about its use.

# Gitcher  

*The git profile switcher*  

![Status](https://img.shields.io/static/v1?label=status&message=production&color=brightgreen "Status: production")    

- Webpage: http://www.borja.glezseoane.es/garaje/gitcher.html
- Mailing list board: http://listas.glezseoane.es/mailman/listinfo/gitcher_listas.glezseoane.es

Gitcher is the git profile switcher. It facilitates the switching between git profiles, importing configuration settings such as name, email and user signatures.

![Screen capture 1](docs/screenshot1.png?raw=true "Screen capture 1")

![Screen capture 2](docs/screenshot2.png?raw=true "Screen capture 2")


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


## What is a Gitcher profile?

A profile is a git configuration data set that includes:

- Name.
- Email.
- PGP Key (optional).
- GPG autosigning preference (activate it do that every commit will be signed).

It is identified by a subject tittle like "work" or "university" that have to be unique.


## Saved data

The `~/.cherfile` file contains the saved profiles data.


## To set up

Please, read the [install guide](./INSTALL.md).


## Acknowledgments

- [Santiago Fernández González](https://github.com/santiagofdezg), for an effusive reception of the tool, being the highest tester of Gitcher after its own author.
- [Arda Kosar](https://github.com/abkosar), for his work on issue [#3](https://github.com/glezseoane/gitcher/issues/3).
- [Mat Kelly](https://github.com/machawk1), for his work with documentation misprints.

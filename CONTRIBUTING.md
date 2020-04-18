# Contributing guide

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

Please, write to González Seoane ([garaje@glezseoane.es](mailto:garaje@glezseoane.es)) for any additional questions or suggestions.

## Mailing lists

Suscribe the mailing list to be updated about the news of Gitcher and to discuss about its development.

Mailing list board: http://listas.glezseoane.es/mailman/listinfo/gitcher_listas.glezseoane.es.



## Suggesting new features

If you find yourself wishing for a feature that doesn't exist in Gitcher, open an issue on our GitHub issues tracker which describes the feature you would like to see, why you need it, and how it should work. Use the `enhancement` label in your issue.



## Bug reports

Open an issue on our GitHub issues list which describes the bug thoroughly. Use the `bug` label in your issue.



## Style guides and conventions

### Code style guide

Gitcher is written in Python, so the PEP-8 rules will be followed to the code standardization. It is highly recommended to use an IDE that revise PEP-8 conventions in your code, as, for example JetBrains's PyCharm.

**Pull request or other type of contributions that not respect PEP-8's conventions could be discarded. The code standardization is a very important part of a good managed software project.**

You can take a look of PEP-8 in the article *[PEP-8: Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)*.

If you don't want to read PEP-8, please observe yet implement code and try to emulate the presentation.


### Git commit messages

- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
- Use the first line as subject line.
- Consider starting the commit message with an applicable tag attending its normal form:
	- `docs:`: documentation.
	- `feat:`: new features.
	- `fix`: fixes of present features.
	- `style`: code cleanliness.
- Limit the first line to 50 characters or less. Start with capital letter and do not close with a dot.
- Add a white line after the subject line.
- Limit all the lines but first to 72 characters or less.
- Reference issues and pull requests liberally after the first line.


### Git branching

This repository follows the [Vincent Driessen's successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/).

The `master` branch is reserved to merges of releases and some documentation changes. The releases are identified with a tag.

Other things will be done in `develop` branch, which can contain other feat-specific branches, if necessary. The release-itself stuff will be done in an `rel-<release-index>` specific branch, then merged in `master` and `develop`.

It is recommended to use `git-workflow` to facilitate the processes. This tools was developed by Vincent Driessen, the author of our Git branching model, so they fit perfectly.

# Contributing guide

The following is a set of guidelines for contributing to this project. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Git commit messages

- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
- Use the first line as subject line.
- Consider starting the commit message with an applicable tag attending its normal form:
	- `docs:`: documentation.
	- `feat:`: new features.
	- `fixes`: fixes of present features.
	- `style`: code cleanliness.
- Limit the first line to 50 characters or less. Start with capital letter and do not close with a dot.
- Add a white line after the subject line.
- Limit all the lines but first to 72 characters or less.
- Reference issues and pull requests liberally after the first line.


## Git branching

This repository follows the [Vincent Driessen's successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/).

The `master` branch is reserved to merges of releases and some documentation changes. The releases are identified with a tag.

Other things will be done in `develop` branch, which can contain other feat-specific branches, if necessary. The release-itself stuff will be done in an `rel-<release-index>` specific branch, then merged in `master` and `develop`.

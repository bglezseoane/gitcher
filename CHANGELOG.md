# Change log

All notable changes to this project will be documented in this file.

## v0.4b0 of 2019-02-23

#### Added

- Update use case option.
- Mirror use case option.
- Fast mode get current active profile option.
- Sort profiles list display.


#### Changed

- Escape command: 'q' by 'quit'. 'q' may be interesting like name or profile 
param.
- Securize and better isolate option validation.
- Relevant performance fixes.


## v0.3b0 of 2019-02-19

#### Added

- Fast mode: use shortcuts to run directly gitcher orders.
- Current git profile status.
- User input validation.
- Cherfile comments support.


#### Changed

- Securize and better isolate model layer operative.
- Fix some performance failures.


## Previous alpha phase

### v0.2a1 of 2019-02-09

#### Changed

This version fixes an error with the set up routine. The necessary libraries were not being imported.


### v0.2a0 of 2019-02-09

#### Added

- Installs the program manpages during the set up routine.


#### Changed

- Improves the software design of the project. Refactors the project as Python package and isolates GITCHER file access to a model layer.
- Improves the user experience with better output printing presentation.


### v0.1a1 of 2019-02-07

#### Changed

Set global option crashed when try to use from a directory that does not contains a git repository. It was by a performance dependencies of 'gitpython' library. The library will be removed from imports and the git commands will be played with operating system calls instead.


### v0.1a0 of 2019-02-05

#### Added

First alpha release. This version is a first approximation of the tool. It covers the entire initial scope of functionalities proposed.


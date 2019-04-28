# Change log

All notable changes to this project will be documented in this file.

## v2.0 of 2019-04-28

This is the first version available to download via Homebrew.

#### Added

- Automatic setup of script endpoint to run the module directly using `$ gitcher` command.
- Interactive mode loop closure.
- Fast mode profiles listing operation.



## v1.3 of 2019-04-16

#### Added

- Profiles list representation switch.



## v1.2.2 of 2019-03-06

#### Changed

- Fix small fails with PyPI distribution.


## v1.2 of 2019-03-06

This is the first version available on PyPI.



## v1.0 of 2019-03-06

This is the first stable version of the program. It is fully tested.

#### Added

- Autocompleter helper support (only for interactive mode).


#### Changed

- Now a dictionary module recopilates every program keys.
- Escape mode: Ctrl.+C is the new method to escape. Command words like 'quit' or 'exit' will not be supported from this version.
- Relevant performance fixes and user experience improvements.



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

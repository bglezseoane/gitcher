# gitcher use cases

A git switcher. It facilitates the switching between git profiles,importing configuration settings such as name, email and user signatures.


## Use cases of gitcher

- [L]: List the preset profiles.
- [S]: Set into an existing repository a configuration profile.
- [G]: Set global a configuration profile.
- [A]: Add a new profile.
- [D]: Delete a profile.
- [U]: Update a profile.
- [C]: Create cherfile.


## Summary of command line possibilities

Use `cher` command to open the interactive console. Once this is done, *gitcher* automatically assert cherfile is reachable. If not, offers you to create it [C]. Then automatically list your preset profiles [L]. Next ask you for orders:

- `s` to set a profile to current directory repository [S].
- `g` to set a profile as global git profile [G].
- `a` to add a new profile [A].
- `u` to update a profile [U].
- `d` to delete a profile [D].
- `q` to quit *gitcher*.


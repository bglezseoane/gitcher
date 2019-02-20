# gitcher use cases

A git switcher. It facilitates the switching between git profiles,importing configuration settings such as name, email and user signatures.


## Use cases of gitcher

- [L]: List the preset profiles.
- [S]: Set into an existing repository a configuration profile.
- [G]: Set global a configuration profile.
- [A]: Add a new profile.
- [M]: Mirror profile (create a copy of a profile with a different name).
- [D]: Delete a profile.
- [U]: Update a profile.
- [C]: Create cherfile.


## Interactive mode

Use `gitcher` command to open the interactive console. Once this is done, 
*gitcher* automatically assert cherfile is reachable. If not, offers you to create it [C]. Then automatically list your preset profiles [L]. Next ask you for orders:

- `s` to set a profile to current directory repository [S].
- `g` to set a profile as global git profile [G].
- `a` to add a new profile [A].
- `u` to update a profile [U].
- `m` to mirror a profile [M].
- `d` to delete a profile [D].
- `q` to quit *gitcher*.


## Fast mode shortcuts

Elementary options are available via command line to avoid gitcher to be 
scriptable and integrable on POSIX systems. To use:

- `gitcher -s <profname>`: [S]'s shortcut.
- `gitcher -g <profname>`: [G]'s shortcut.
- `gitcher -a <profname> <name> <email> <signkey or 'None'> <'True' or 
'False' as signpref>`: 
[A]'s shortcut.
- `gitcher -d <profname>`: [D]'s shortcut.

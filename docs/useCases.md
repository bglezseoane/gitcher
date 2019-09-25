# gitcher use cases

A git switcher. It facilitates the switching between git profiles,importing configuration settings such as name, email and user signatures.


## Use cases of Gitcher

- [L]: List the preset profiles.
- [O]: See currently active (ON) profile.
- [S]: Set into an existing repository a configuration profile.
- [G]: Set global a configuration profile.
- [A]: Add a new profile.
- [M]: Mirror profile (create a copy of a profile with a different name).
- [D]: Delete a profile.
- [U]: Update a profile.
- [C]: Create cherfile.


## Interactive mode

Use `gitcher` command to open the interactive console. Once this is done, 
Gitcher automatically assert cherfile is reachable. If not, create it [C]. Then automatically list your preset profiles [[L], [O]]. Next 
ask you for orders:

- `s` to set a profile to current directory repository [S].
- `g` to set a profile as global git profile [G].
- `a` to add a new profile [A].
- `u` to update a profile [U].
- `m` to mirror a profile [M].
- `d` to delete a profile [D].
- `Ctrl.+C` to quit *gitcher*.


## Fast mode shortcuts

Elementary options are available via command line to allow Gitcher to be 
scriptable and integrable on POSIX systems. To use:

- `gitcher -l`: [L]'s shortcut.
- `gitcher -o`: [O]'s shortcut.
- `gitcher -s <profname>`: [S]'s shortcut.
- `gitcher -g <profname>`: [G]'s shortcut.
- `gitcher -a <profname> <name> <email> <signkey or 'None'> <'True' or 
'False' as signpref>`: 
[A]'s shortcut.
- `gitcher -d <profname>`: [D]'s shortcut.

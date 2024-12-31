# Concern
Control pym2149 (via Lurlene) or FoxDot using Vim

## Install
These are generic installation instructions.

### To use, disposably
Install the current release from PyPI to a virtual environment:
```
python3 -m venv venvname
venvname/bin/pip install -U pip
venvname/bin/pip install Concern
. venvname/bin/activate
```
You will also need one of the following backends.

#### FoxDot backend
```
# Simply install, and Concern will use it:
venvname/bin/pip install FoxDot
```

#### pym2149 backend
```
# Install as usual:
venvname/bin/pip install pym2149

# Tell Concern to use it instead of foxdot:
echo Concern consumerName = pym2149 | tee -a ~/.settings.arid
```

### To use, permanently
```
# Tested on Linux and Mac:
pip3 install --user Concern
```
To add a backend, substitute `pip3 install --user` for `venvname/bin/pip install` above.
See `~/.local/bin` for executables.

### To develop
First install venvpool to get the `motivate` command:
```
pip3 install --user venvpool
```
Get codebase and install executables:
```
git clone git@github.com:combatopera/Concern.git
motivate Concern
```
Requirements will be satisfied just in time, using sibling projects with matching .egg-info if any.

## Commands

### Concern
Vim-based live coding environment.

## Usage

### FoxDot
```
# Any arguments are passed to vim, here we discover the FoxDot demo directory:
Concern "$(venvname/bin/python -c 'from pkg_resources import resource_filename; print(resource_filename("FoxDot", "demo"))' | tail -1)"
```
* FoxDot is running in the right hand third of the screen
* Send code to FoxDot by typing backslash followed by `]`
    * This will send the smallest top-level suite under the cursor
    * The backslash is actually your Vim leader key
* Use visual mode to send multiple top-level suites at once
* Use backslash enter instead of backslash `]` to send from cursor to the end of the file
* Use backslash `q` to quit all of Vim, FoxDot and GNU Screen

### pym2149
```
# Download some files to play with:
git clone git@github.com:combatopera/pym2149.git

# Load a non-trivial tune written in the Lurlene live coding language:
Concern 'pym2149/contrib/Lemmings 2 Tune 6.py'
```
* Once pym2149 has initialised, type backslash enter at the top of the file to send the whole program

# Concern
Control pym2149 (via Lurlene) or FoxDot using Vim

## Install
These are generic installation instructions.

### To use, permanently
The quickest way to get started is to install the current release from PyPI:
```
# Tested on Linux and Mac:
pip3 install --user Concern
```
You will also need one of the following backends.

#### FoxDot backend
```
# Simply install, and Concern will use it:
pip3 install --user FoxDot
```

#### pym2149 backend
```
# Install as usual:
pip3 install --user pym2149

# Tell Concern to use it instead of foxdot:
echo Concern consumerName = pym2149 | tee -a ~/.settings.arid
```

### To use, temporarily
If you prefer to keep .local clean, install to a virtualenv:
```
python3 -m venv venvname
venvname/bin/pip install Concern
. venvname/bin/activate
```
To add a backend, substitute `pip install` for `pip3 install --user` above.

### To develop
First clone the repo using HTTP or SSH:
```
git clone https://github.com/combatopera/Concern.git
git clone git@github.com:combatopera/Concern.git
```
Now use pyven's pipify to create a setup.py, which pip can then use to install the project editably:
```
python3 -m venv pyvenvenv
pyvenvenv/bin/pip install pyven
pyvenvenv/bin/pipify Concern

python3 -m venv venvname
venvname/bin/pip install -e Concern
. venvname/bin/activate
```

## Commands

### Concern
Vim-based live coding environment.

## Usage

### FoxDot
```
# Any arguments are passed to vim, here we discover the FoxDot demo directory:
Concern "$(python3 -c 'from pkg_resources import resource_filename; print(resource_filename("FoxDot", "demo"))' | tail -1)"
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
# GitHub trick to download some files to play with:
svn export https://github.com/combatopera/pym2149/trunk/contrib

# Load a non-trivial tune written in the Lurlene live coding language:
Concern 'contrib/Lemmings 2 Tune 6.py'
```
* Once pym2149 has initialised, type backslash enter at the top of the file to send the whole program

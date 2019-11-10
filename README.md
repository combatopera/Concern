# Concern
Use Vim to control FoxDot or pym2149 with the aid of GNU Screen.

[![Build Status](https://travis-ci.org/combatopera/Concern.svg?branch=master)](https://travis-ci.org/combatopera/Concern)

## Install latest release
```
# Tested on Linux and Mac:
pip3 install --user Concern
```
You will also need one of the following backends.

### FoxDot backend
```
# Simply install, and Concern will use it:
pip3 install --user FoxDot
```
### pym2149 backend
```
# Install as usual:
pip3 install --user pym2149

# Tell Concern to use it instead of foxdot:
echo Concern consumerName = pym2149 | tee -a ~/.settings.arid
```
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

# Load a non-trivial tune written in pym2149's (currently nameless) live coding language:
Concern 'contrib/Lemmings 2 Tune 6.py'
```
* Once pym2149 has initialised, type backslash enter at the top of the file to send the whole program

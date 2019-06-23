# Concern

Use Vim to control FoxDot with the aid of GNU Screen.

## Install

* Get the latest zip file from <https://github.com/combatopera/Concern/releases/latest>
* You'll also need a clone of the [FoxDot GitHub repository](https://github.com/qirky/FoxDot)
    * An existing setup.py install of FoxDot can't be used

### Config

* Create a file `.settings.arid` in your home directory (note the initial dot)
* Add a line specifying the location of your FoxDot repository as follows

> `Concern foxdot home = /path/to/FoxDot`

### Linux

* `sudo apt-get install python3-tk python3-venv python3-pyparsing screen vim`
* `unzip` the zip file you downloaded
* `cd` into the directory
* `./Concern`
    * The first run will automatically build a Virtualenv, subsequent launches will be faster
    * Any arguments passed into `Concern` are forwarded to Vim
    * The default action is to show the FoxDot `demo` directory

## Usage

* FoxDot is running in the right hand third of the screen
* Send code to FoxDot by typing backslash followed by enter
    * This will send the smallest top-level suite under the cursor
    * The backslash is actually your Vim leader key
* Use visual mode to send multiple top-level suites at once
* To quit you will need to terminate both Vim and FoxDot manually
    * Use ctrl a followed by n to navigate to the next GNU Screen window

## Support

* Tweet me at <https://twitter.com/combatopera>

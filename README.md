# Concern

Use Vim to control FoxDot or pym2149 with the aid of GNU Screen.

## Install

* Get the latest zip file from <https://github.com/combatopera/Concern/releases/latest>

## Usage

* FoxDot is running in the right hand third of the screen
* Send code to FoxDot by typing backslash followed by enter
    * This will send the smallest top-level suite under the cursor
    * The backslash is actually your Vim leader key
* Use visual mode to send multiple top-level suites at once
* Use backslash `]` instead of backslash enter to send from cursor to the end of the file
* To quit you will need to terminate both Vim and FoxDot manually
    * Use ctrl a followed by n to navigate to the next GNU Screen window

## pym2149

* To target pym2149 instead of FoxDot add the following to your `.settings.arid`

> `Concern consumerName = pym2149`

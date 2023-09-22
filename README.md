# Hybrid Control
Hybrid test stand control software.

## Getting Started
1. Download the [LJM Software](https://labjack.com/pages/support?doc=%2Fsoftware-driver%2Finstaller-downloads%2Fljm-software-installers-t4-t7-digit%2F)
2. Download the Python wrapper for the LJM library: `python -m pip install labjack-ljm`, where `python` is your usual Python interpreter
3. Run `src/main.py`

## Running
`quit` or <kbd>esc</kbd> to quit the program.
### Usage
```zsh
[valve] [num] [on/off]
```
### Options
Available valves: `mav`, `srbv`, `sv`

Valve numbers `1-5` for `sv`

## Useful Links
- [LabJack PWM pseudocode generator](https://labjack.com/pages/support/?doc=%2Fdatasheets%2Ft-series-datasheet%2F1322-pwm-out-t-series-datasheet%2F)

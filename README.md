# Hybrid Control
Hybrid test stand control software.

## Getting Started
1. Download the [LJM Software](https://labjack.com/pages/support?doc=%2Fsoftware-driver%2Finstaller-downloads%2Fljm-software-installers-t4-t7-digit%2F)
2. Download the Python wrapper for the LJM library: `python -m pip install labjack-ljm`, where `python` is your usual Python interpreter (*For unit tests*)
3. Download ```cmake``` with a package manager of your choice


## Running
*When running while connected to the LabJack, make sure that* ```add_definitions(-DUSE_LABJACK)``` *is uncommented in the ```CMakeLists.txt``` file.*
1. Create a top-level ```build/``` directory
2. Run ```cmake ..``` from within ```build/```
3. Run ```make```
4. Run ```./hybrid```

Note: On macOS, you may have to manually set your ```DYLD_LIBRARY_PATH```, such as ```export DYLD_LIBRARY_PATH=/usr/local/lib/```
   
### Usage
```zsh
[valve] [num] [on/off]
```
### Options
Available valves: `mav`, `sv`

Valve numbers `1-5` for `sv`

## Useful Links
- [LabJack PWM pseudocode generator](https://labjack.com/pages/support/?doc=%2Fdatasheets%2Ft-series-datasheet%2F1322-pwm-out-t-series-datasheet%2F)
- [LabJack function reference](https://labjack.com/pages/support/?doc=/software-driver/ljm-users-guide/function-reference/)

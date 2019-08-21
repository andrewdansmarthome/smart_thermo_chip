# smart_thermo_chip

This whole project is in its nascent stages! We are building a physical NEST-like themostat and integrating it with a functional web-app to view status and control/schedule the thermostat. Stretch goals are to add some learning capabilities and start adding in additional functionalities that are more hub-like. Voice activation? Connect with chromecast/speakers? Limitless possibilities.

Lots on the to-do list.

To-Do:
- Add minimum allowable temperature reading or force furnace on
- Add max length of furnace run time
- Add better control of furnace run times via config
- Gracefully handle shutdown to TURN OFF THE FURNACE when it fails
- ????
- Profit

Done:
- Set override for ioTestToggle button so it doesn't keep switching every cycle
- Add 10nf capacitor across sensor to ground to stabilize (and range correct) readings
- Refactoring complete!!!
- Test integration with RPi once re-structure is complete.
- Restructure app to OO architecture broken out into classes.
- Write Config method to get config from server
- Write Scheduler method to get schedule from the server
- Write Temperature class to store and bundle data to send to the server

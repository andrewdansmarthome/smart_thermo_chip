# smart_thermo_chip

This whole project is in its nascent stages! We are building a physical NEST-like themostat and integrating it with a functional web-app to view status and control/schedule the thermostat. Stretch goals are to add some learning capabilities and start adding in additional functionalities that are more hub-like. Voice activation? Connect with chromecast/speakers? Limitless possibilities.

Lots on the to-do list.

To-Do:
- Test integration with RPi once re-structure is complete.
- Add 10nf capacitor across sensor to ground to stabilize (and range correct) readings
- ????
- Profit

Done: 
- Restructure app to OO architecture broken out into classes.
- Write Config method to get config from server
- Write Scheduler method to get schedule from the server
- Write Temperature class to store and bundle data to send to the server

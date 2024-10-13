PiCar Project

This project involves configuring a Raspberry Pi to control a remote-controlled (RC) car, with a gaming wheel and pedals connected to a PC. 
The PC accesses a web interface hosted by a Flask server running on the Raspberry Pi, enabling control of the RC car.

Features

Raspberry Pi controlled RC Car: The car is controlled by commands sent to the Raspberry Pi, which handles motor operations.
Gaming wheel and pedals integration: The gaming wheel and pedals are connected to a PC, which interacts with the web interface hosted by the Flask server.
Web Interface: The control panel is accessible from any device connected to the network, providing remote control functionality.

Project Setup

Hardware Requirements:
Raspberry Pi (any version with GPIO support)
RC car with electronic speed control
Gaming wheel and pedals connected to a PC
Power supply for Raspberry Pi
Wi-Fi module (if not integrated with your Raspberry Pi model)
PC to interact with the web interface

Software Requirements:
Raspbian OS (or any Linux-based system compatible with the Raspberry Pi)
Python 3.x
Flask for the web interface
Additional Python libraries (e.g., RPi.GPIO for GPIO control)

Wiring the Raspberry Pi:
Connect the RC car’s motors and controls to the GPIO pins on the Raspberry Pi.

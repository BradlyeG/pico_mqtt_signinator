## The Signinator

I want a sign hanging on my office door, whose text can be updated with a simple MQTT message. The message can be sent with whatever script and that's more or less that. This project is intended as a self-hosted solution and is developed with the Eclipse Mosquitto broker. The target board is a Pi Pico W.

The development platform at present is a HUB75 64x64 LED Matrix from WaveShare

## TODO
Configure TLS

Refactor terminal app to something more useful
  Custom text input and color
  Quick options for status display (Out of office, busy, on a call, etc)
  Eventually build options for provisioning more signs (input board type and display parameters, output code.py)

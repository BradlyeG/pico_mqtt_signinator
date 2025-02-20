## The Signinator

I want a sign hanging on my office door, whose text can be updated with a simple MQTT message. The message can be sent with whatever script and that's more or less that. This project is intended as a self-hosted solution and is developed with the Eclipse Mosquitto broker. The target board is a Pi Pico W.

The development platform at present is a HUB75 64x64 LED Matrix from WaveShare

## TODO
Finish rebasing to circuitpython

Cache message on successful receipt and check if most recent message differs from cache

Configure TLS for Mosquitto

Sign should be topic observe

Refactor terminal app to take parameters instead of asking for input

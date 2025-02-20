## The Signinator

I want a sign hanging on my office door, whose text can be updated with a simple MQTT message. The message can be sent with whatever script and that's more or less that. This project is intended as a self-hosted solution and is developed with the Eclipse Mosquitto broker. The target board is a Pi Pico W.

The development platform at present is an Adafruit 1.3" Color TFT Screen (ST7789), but will also later use the Adafruit 64x32 LED Matrix. It requires the Arduino WiFi 101, Adafruit GFX, and Arduino-MQTT libraries.

## TODO
Finish rebasing to circuitpython

Cache message on successful receipt and check if most recent message differs from cache

Configure TLS for Mosquitto

Sign should be topic observe

Refactor terminal app to take parameters instead of asking for input

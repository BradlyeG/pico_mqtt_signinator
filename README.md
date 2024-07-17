The idea is I have a sign hanging on my office door, whose text can be updated with a simple MQTT message. The message can be sent with whatever script and that's more or less that.

This project is intended as a self-hosted solution and is developed with the Eclipse Mosquitto broker. The target board at present is an Adafruit Feather M0 WiFi (SAMD21 & WINC1500) on the arduino platform.

The development platform starts with an Adafruit 1.3" Color TFT Screen (ST7789), but will also later use the Adafruit 64x32 LED Matrix. It requires the Arduino WiFi 101, Adafruit Protomatter, and Adafruit GFX libraries.

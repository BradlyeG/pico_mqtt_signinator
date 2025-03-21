## The Signinator

I want a sign hanging on my office door, whose text can be updated with a simple MQTT message. The message can be sent with whatever script and that's more or less that. This project is intended as a self-hosted solution and is developed with the Eclipse Mosquitto broker. The target board is a Pi Pico W.

The development platform at present is a HUB75 64x64 LED Matrix from WaveShare

## TODO
Configure TLS

Refactor terminal app to a GUI tool for better administration of signs
  
Create Provision GUI tool to quickly create new signs

Continue testing board code

## Dependencies
The following libraries are not on the development board by default - they can be downloaded from the adafruit circuitpython bundle or community circuitpython bundle

adafruit_display_text

adafruit_minimqtt

adafruit_ticks

adafruit_connection_manager

adafruit_ntp

cptoml (https://github.com/beryllium-org/cptoml)

Display driver - While RGB matricies can generally use rgbmatrix (which is built in) most displays will have some kind of controller and a specific library, like ST7789 or ILI9341

## Definitions
Inside GUI and Board Code folders are directories named according to the board configuration they represent:

    board_name-interface-display (ex. pipw-adafruit2345-hub75_64x64)
    Pi Pico W + adafruit product 2345 as the interface + HUB75 64x64 LED Matrix
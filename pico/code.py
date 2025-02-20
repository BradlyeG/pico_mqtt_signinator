import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import os
import ipaddress
import wifi
import socketpool

# Release displays first
displayio.release_displays()

# Cofiguration Options
# TODO - Move to external txt file or something
width_value = 64
height_value = 64
bit_depth_value = 3
chain_height = 1
serpentine_value = True

matrix = rgbmatrix.RGBMatrix(
   width = os.getenv('WIDTH'), height = os.getenv('HEIGHT'), bit_depth = os.getenv('BIT_DEPTH'),
   rgb_pins = [board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
   addr_pins = [board.GP10, board.GP16, board.GP18, board.GP20, board.GP22],
   clock_pin = board.GP11, latch_pin = board.GP12, output_enable_pin = board.GP13,
   tile = os.getenv('CHAIN_HEIGHT'), serpentine = os.getenv('SERPENTINE'),
   doublebuffer = True)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

print("Connecting to Wifi...")

try:
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
except TypeError:
    print("Unable to load WiFi info. Check settings.toml")
    raise

print("Connected to WiFi")

pool = socketpool.SocketPool(wifi.radio)

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

print("My IP addr:", wifi.radio.ipv4_address)

google_ipv4 = ipaddress.ip_address("8.8.4.4")

while True:
    display.refresh(minimum_frames_per_second=0)
    print("Ping google.com: %f ms" & (wifi.radio.ping(google_ipv4)*1000))
    time.sleep(5)

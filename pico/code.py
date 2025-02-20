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
import time

# Release displays first
displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
   width = os.getenv('unit_width') * os.getenv('chain_width'), height = os.getenv('unit_height') * os.getenv('chain_height') , bit_depth = os.getenv('bit_depth'),
   rgb_pins = [board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
   addr_pins = [board.GP10, board.GP16, board.GP18, board.GP20, board.GP22],
   clock_pin = board.GP11, latch_pin = board.GP12, output_enable_pin = board.GP13,
   tile = os.getenv('chain_height'), serpentine = eval(os.getenv('serpentine')),
   doublebuffer = True)
# Tile should be pulled from CHAIN_HEIGHT var in settings but keeps throwing a value error

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

print("Connecting to Wifi...")
display.refresh(minimum_frames_per_second=0)

try:
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
except TypeError:
    print("Unable to load WiFi info. Check settings.toml")
    raise

print("Connected to WiFi")
display.refresh(minimum_frames_per_second=0)

pool = socketpool.SocketPool(wifi.radio)

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
display.refresh(minimum_frames_per_second=0)
time.sleep(0.5)

print("My IP addr:", wifi.radio.ipv4_address)
display.refresh(minimum_frames_per_second=0)
time.sleep(0.5)

google_ipv4 = ipaddress.ip_address("8.8.4.4")

while True:
    print("Ping google.com: %f ms" % (wifi.radio.ping(google_ipv4)*1000))
    display.refresh(minimum_frames_per_second=0)
    time.sleep(5)

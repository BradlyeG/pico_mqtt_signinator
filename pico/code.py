import adafruit_display_text.text_box as text_box
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import os
import ipaddress
import wifi
import adafruit_connection_manager
import time
import adafruit_minimqtt.adafruit_minimqtt as MQTT

# Release displays first
displayio.release_displays()

# Declare matrix device
matrix = rgbmatrix.RGBMatrix(
   width = os.getenv('unit_width') * os.getenv('chain_width'), height = os.getenv('unit_height') * os.getenv('chain_height') , bit_depth = os.getenv('bit_depth'),
   rgb_pins = [board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
   addr_pins = [board.GP10, board.GP16, board.GP18, board.GP20, board.GP22],
   clock_pin = board.GP11, latch_pin = board.GP12, output_enable_pin = board.GP13,
   tile = os.getenv('chain_height'), serpentine = eval(os.getenv('serpentine')),
   doublebuffer = True)

# Assign the matrix to a display that can be manipulated
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# MQTT Callback methods for when events occur
def connected(client, userdata, flags, rc):
    # Called when the client is connected successfully to broker
    print(f"Connected to broker. Listening for changes on {os.getenv('client_topic')}")
    client.subscribe(os.getenv('client_topic'))

def disconnected(client, userdata, rc):
  # Called when client is disconnected
  print("Disconnected from broker")

def message(client, topic, message):
   """Called when client has a new message from subscribed topic.
   :param str topic: Topic with new value
   :param str message: The new value
   """
   display.root_group = None
   display_text = text_box.TextBox(terminalio.FONT,
        text = message,
        color = 0xFFFFFF,
        width = os.getenv('unit_width'),
        height = os.getenv('unit_height'),
        align = text_box.TextBox.ALIGN_LEFT
    )
   display_text.anchor_point = (0,0)
   display_text.anchored_position = (0,0)
   display.root_group = display_text
   display.refresh()

# Connect to WiFi
print("Connecting to Wifi...")
display.refresh()

try:
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
except TypeError:
    print("Unable to load WiFi info. Check settings.toml")
    raise

print("Connected to WiFi")
display.refresh(minimum_frames_per_second=0)

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
display.refresh()
time.sleep(0.5)

print("My IP addr:", wifi.radio.ipv4_address)
display.refresh()
time.sleep(0.5)

mqtt_client = MQTT.MQTT(
    broker=os.getenv('broker_ip'),
    port=os.getenv('broker_port'),
    username=os.getenv('uname'),
    password=os.getenv('pass'),
    client_id=os.getenv('client_id'),
    is_ssl=False,
    socket_pool=pool,
    ssl_context=ssl_context,
)

# Set callback methods
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

mqtt_client.connect()

while True:
    mqtt_client.loop()
    time.sleep(1)

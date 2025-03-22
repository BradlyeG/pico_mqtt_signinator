import time
import wifi
import alarm
import board
import digitalio
import displayio
import framebufferio
import ipaddress
import rgbmatrix
import terminalio
import adafruit_ntp
import adafruit_connection_manager
import adafruit_display_text.text_box as text_box
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from cptoml import fetch
from cptoml import put
from storage import remount

# Get all the env variables that get read multiple times
unit_width = fetch('unit_width')
unit_height = fetch('unit_height')
client_topic = fetch('client_topic')
bedtime_hr = fetch('bedtime_hr')
bedtime_min = fetch('bedtime_min')
wake_hr = fetch('wake_hr')
wake_min = fetch('wake_min')
last_sleep_day = fetch('last_sleep_day')
use_bedtime = fetch('use_bedtime')
sleep_duration_seconds = fetch('sleep_duration_seconds')

# Release displays first
displayio.release_displays()

# Declare matrix device
matrix = rgbmatrix.RGBMatrix(
   width = unit_width * fetch('chain_width'), 
   height = unit_height * fetch('chain_height') , 
   bit_depth = fetch('bit_depth'),
   rgb_pins = [board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
   addr_pins = [board.GP10, board.GP16, board.GP18, board.GP20, board.GP22],
   clock_pin = board.GP11, latch_pin = board.GP12, output_enable_pin = board.GP13,
   tile = fetch('chain_height'), serpentine = eval(fetch('serpentine')),
   doublebuffer = True)

# Assign the matrix to a display that can be manipulated
display = framebufferio.FramebufferDisplay(matrix, rotation = fetch('rotation'), auto_refresh=False)

# MQTT Callback methods for when events occur
def connected(client, userdata, flags, rc):
    # Called when the client is connected successfully to broker
    print(f"Connected to broker. Listening for changes on {fetch('client_topic')}")
    client.subscribe(fetch('client_topic'))

def disconnected(client, userdata, rc):
  # Called when client is disconnected
  print("Disconnected from broker")

def message(client, topic, message):
   """Called when client has a new message from subscribed topic.
   :param str topic: Topic with new value
   :param str message: The new value
   """
   try:
        raw_col = int(("0x" + message[:6]))
   except:
        raw_col = 0xFFFFFF
   display.root_group = None
   display_text = text_box.TextBox(terminalio.FONT,
        text = message[6:],
        color = raw_col,
        width = unit_width,
        height = unit_height,
        align = text_box.TextBox.ALIGN_LEFT
    )
   display_text.anchor_point = (0,0)
   display_text.anchored_position = (0,0)
   display.root_group = display_text
   display.refresh()

def is_bedtime(hr, mn, day):
    if hr >= bedtime_hr and hr <= wake_hr:
        if mn >= bedtime_min and mn < wake_min:
            if day != last_sleep_day:
                remount("/", False)
                put('last_sleep_day', current_day)
                remount("/", True)
                displayio.release_displays()
                alarm.exit_and_deep_sleep_until_alarms(alarm.time.TimeAlarm(monotonic_time = time.monotonic() + sleep_duration_seconds))

# Connect to WiFi
print("Connecting to Wifi...")
display.refresh()

try:
    wifi.radio.connect(fetch('CIRCUITPY_WIFI_SSID'), fetch('CIRCUITPY_WIFI_PASSWORD'))
except TypeError:
    print("Unable to load WiFi info. Check settings.toml")
    raise

print("Connected to WiFi")
display.refresh(minimum_frames_per_second=0)

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset = 0, cache_seconds = 3600)

current_time = ntp.datetime
current_day = current_time[2]

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
display.refresh()
time.sleep(0.5)

print("My IP addr:", wifi.radio.ipv4_address)
display.refresh()
time.sleep(0.5)

mqtt_client = MQTT.MQTT(
    broker=fetch('broker_ip'),
    port=fetch('broker_port'),
    username=fetch('uname'),
    password=fetch('pass'),
    client_id=fetch('client_id'),
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
    current_time = ntp.datetime
    if eval(use_bedtime):
        is_bedtime(current_time[3], current_time[4], current_day)
    time.sleep(15)

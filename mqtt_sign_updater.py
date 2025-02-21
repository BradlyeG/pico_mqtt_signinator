import time
from paho.mqtt import client as mqtt_client

# Configuration options
BROKER = "broker_address"
PORT = 1883
CLIENT_ID = "Python Sign Updater"
USERNAME = "username"
PASSWORD = "password"
TOPIC = "your-sign-topic"

def connect_mqtt():
    """
    Function to handle connecting to broker and associated helper functions.
    
    Args:
        None

    Returns:
        None
    """
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("\nConnected to MQTT Broker!")
        else:
            print("\nFailed to connect, return code %d\n", rc)

    # Set client ID
    client = mqtt_client.Client(client_id=CLIENT_ID, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    # Set uname/pass and then connect
    client.username_pw_set(USERNAME, PASSWORD)
    #client.tls_set('./certs/ca.crt')
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client

def run():
    """
    Main Runner Function

    Args:
        None

    Returns:
        None
    """
    print("\t****************************************")
    print("\t***         MQTT Sign Updater        ***")
    print("\t****************************************")

    client = connect_mqtt()
    client.loop_start()
    # Wait to make sure we are connected before proceeding
    while not client.is_connected():
        time.sleep(0.1)
    message = input("\nPlease enter brief message to display on sign: ")
    client.publish(TOPIC, message, qos=1)
    client.disconnect()
    client.loop_stop()

if __name__ == '__main__':
    run()
   
from paho.mqtt import client as mqtt_client

# Configuration options
broker = "broker_address"
port = 1883
client_id = "Python Sign Updater"
username = "username"
password = "password"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("\nConnected to MQTT Broker!")
        else:
            print("\nFailed to connect, return code %d\n", rc)       

    # Set client ID
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    # Set uname/pass and then connect
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def run():
    print("\t****************************************")
    print("\t***         MQTT Sign Updater        ***")
    print("\t****************************************")

    client = connect_mqtt()
    client.loop_start()
    # Wait to make sure we are connected before proceeding
    while not client.is_connected():
        time.sleep(0.1)
    message = input("\nPlease enter brief message to display on sign: ")
    topic = input("\nPlease enter the topic the sign is subsribed to: ")
    pub_msg = client.publish(topic, message, qos=1)
    client.disconnect()
    client.loop_stop()

if __name__ == '__main__':
    run()
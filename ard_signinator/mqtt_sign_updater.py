from paho.mqtt import client as mqtt_client

# Configuration options
broker = "broker_address"
port = 1883
topic = "signs/GF_Office"
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
    client = mqtt_client.client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    # Set uname/pass and then connect
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_publish(client, userdata, mid, reason_code, properties):
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")


def run():
    print("\t****************************************")
    print("\t***         MQTT Sign Updater        ***")
    print("\t****************************************")

    unacked_publish = set()

    client = connect_mqtt()
    client.loop_start()
    message = input("\nPlease enter brief message to display on sign")
    topic = input("\nPlease enter the topic the sign is subsribed to")
    pub_msg = client.publish(topic, message, qos=1)

if __name__ == '__main__':
    run()

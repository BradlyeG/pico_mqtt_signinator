
// Pin Definitions for the screen
#define D_CS A3
#define D_RST A4
#define D_DC A5
#define BROKER_IP "0.0.0.0" //IP address of MQTT broker
#define CLIENT_ID "Ground Office" //ID that will be used to connect to broker
#define UNAME "public" // Username that will be used to connect to broker
#define PASS "public" // Password that will be used to connect to broker
#define CLIENT_TOPIC "signs/gf_sign" // Configure what topic corresponds to this sign

#include <Adafruit_GFX.h> //Graphics library
#include <Adafruit_ST7789.h> //Hardware library for ST7789 display
#include <WiFi101.h> //WiFi library
#include <MQTT.h> // MQTT Client library
#include <SPI.h>

#include "arduino_secrets.h" //Used to store private wifi credentials

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
int status = WL_IDLE_STATUS;

//Create the display
Adafruit_ST7789 display = Adafruit_ST7789(D_CS, D_DC, D_RST);

//Create WiFi device and MQTT client
WiFiClient wifi;
MQTTClient client;

void setup(void){
  //Configure pins for Adafruit ATWINC1500 Feather
  WiFi.setPins(8,7,4,2);
  Serial.begin(9600);
  WiFi.begin(ssid, pass);
  while(!Serial){
    ; //wait for serial
  }
  //Need to initialize display and set text options
  display.init(240, 240);
  display.fillScreen(0x000000);
  display.setCursor(0, 0);
  display.setTextColor(0xFFFFFF);
  display.setTextSize(2);
  display.setTextWrap(true);

  //Initialize client and connect to broker
  client.begin(BROKER_IP, wifi);
  client.onMessage(messageReceived);
  connect();

}

void loop(void){
  client.loop();

  if(!client.connected()){
    connect();
  }
}

void printWiFiData() {
  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  display.println("IP Address: ");
  display.println(ip);

  // print your MAC address:
  byte mac[6];
  WiFi.macAddress(mac);
  display.println("MAC address: ");
  printMacAddress(mac);

}

void printCurrentNet() {
  // print the SSID of the network you're attached to:
  display.println("SSID: ");
  display.println(WiFi.SSID());

  // print the MAC address of the router you're attached to:
  byte bssid[6];
  WiFi.BSSID(bssid);
  display.println("BSSID: ");
  printMacAddress(bssid);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  display.println("signal strength (RSSI):");
  display.println(rssi);

  // print the encryption type:
  byte encryption = WiFi.encryptionType();
  display.println("Encryption Type:");
  display.println(encryption, HEX);
  display.println();
}

void printMacAddress(byte mac[]) {
  for (int i = 5; i >= 0; i--) {
    if (mac[i] < 16) {
      display.print("0");
    }
    display.print(mac[i], HEX);
    if (i > 0) {
      display.print(":");
    }
  }
  display.println();
}

void connect(){
  // attempt to connect to WiFi network:
  while ( status != WL_CONNECTED) {
    display.println("Attempting to connect to WPA SSID: ");
    display.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);
    display.println("Waiting 10 seconds for connection...");
    // wait 3 seconds for connection:
    delay(3000);
      // print out network information
    display.println("WiFi Connection success!");
  }
  
  display.fillScreen(0x000000);
  display.setCursor(0, 0);
  display.println("Trying to connect to broker...");
  // Wait for connection to broker
  while (!client.connect(CLIENT_ID, UNAME, PASS)){
    display.print(".");
    delay(250);
  }
  
  display.println("Connected to broker!");
  client.subscribe(CLIENT_TOPIC);
  display.println("Subscribed to topic");
  display.println("Awaiting sign message...");
}

void messageReceived(String &topic, String &payload){
  display.fillScreen(0x000000);
  display.setCursor(0, 0);
  display.println(payload);
}
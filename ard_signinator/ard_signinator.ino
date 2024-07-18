
// Pin Definitions for the screen
#define D_CS A3
#define D_RST A4
#define D_DC A5

#include <Adafruit_GFX.h> //Graphics library
#include <Adafruit_ST7789.h> //Hardware library for ST7789 display
#include <WiFi101.h> //WiFi library
#include <SPI.h>

#include "arduino_secrets.h" //Used to store private wifi credentials

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
int status = WL_IDLE_STATUS;

//Create the display
Adafruit_ST7789 display = Adafruit_ST7789(D_CS, D_DC, D_RST);

void setup(void){
  //Configure pins for Adafruit ATWINC1500 Feather
  WiFi.setPins(8,7,4,2);
  Serial.begin(9600);
  while(!Serial){
    ; //wait for serial
  }
  display.init(240, 240);

  // attempt to connect to WiFi network:
  while ( status != WL_CONNECTED) {
    display.println("Attempting to connect to WPA SSID: ");
    display.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);
    display.println("Waiting 10 seconds for connection...");
    // wait 10 seconds for connection:
    delay(10000);
  }

  // print out network information
  display.println("Connection success!");
  printCurrentNet();
  printWiFiData();


}

void loop(void){

}

void printWiFiData() {
  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  display.print("IP Address: ");
  display.println(ip);
  display.println(ip);

  // print your MAC address:
  byte mac[6];
  WiFi.macAddress(mac);
  display.print("MAC address: ");
  printMacAddress(mac);

}

void printCurrentNet() {
  // print the SSID of the network you're attached to:
  display.print("SSID: ");
  display.println(WiFi.SSID());

  // print the MAC address of the router you're attached to:
  byte bssid[6];
  WiFi.BSSID(bssid);
  display.print("BSSID: ");
  printMacAddress(bssid);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  display.print("signal strength (RSSI):");
  display.println(rssi);

  // print the encryption type:
  byte encryption = WiFi.encryptionType();
  display.print("Encryption Type:");
  display.println(encryption, HEX);
  Serial.println();
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
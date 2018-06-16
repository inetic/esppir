#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <list>

#include "discovery.h"
#include "wifi_credentials.h" // Defines WIFI_SSID and WIFI_PASS

int ledPin = 1;  // LED on Pin 13 of Arduino
int pirPin = 0; // Input for HC-S501

const uint16_t SERVER_PORT = 4500;
WiFiServer server(SERVER_PORT);
Discovery discovery;

void setup()
{
    pinMode(pirPin, INPUT);

    //for (int i = 0; i < 10; i++) {
    //  digitalWrite(ledPin, LOW);
    //  delay(200);
    //  digitalWrite(ledPin, HIGH);
    //  delay(200);
    //}

    //digitalWrite(ledPin, HIGH);

    //------------------------------------------
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    while (WiFi.status() != WL_CONNECTED) { delay(500); }

    //------------------------------------------
    server.begin();
    discovery.start(3210);
    discovery.add_service("esppir", (WiFi.localIP().toString() + ":" + String(SERVER_PORT)).c_str());
}

unsigned long next_hello = 0;

std::list<WiFiClient> clients;

static void remove_disconnected_clients()
{
    for (auto i = clients.begin(); i != clients.end();) {
        auto j = std::next(i);
        if (!i->connected()) clients.erase(i);
        i = j;
    }
}

void loop()
{
    discovery.update();

    int pirValue = digitalRead(pirPin);

    WiFiClient client = server.available();

    if (client) {
        clients.push_back(client);
    }

    if (millis() >= next_hello) {
        remove_disconnected_clients();

        for (auto& c : clients) {
            c.printf("client-count:%d pir-value:%d", clients.size(), pirValue);
        }

        next_hello = millis() + 200;
    }

    delay(20);
}

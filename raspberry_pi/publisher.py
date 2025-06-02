import paho.mqtt.client as mqtt
import Adafruit_DHT
import time
import json

# ΡΥΘΜΙΣΕΙΣ
MQTT_BROKER = "192.168.1.2"  # IP του Mosquitto Broker (υπολογιστής με Docker)
DEVICE_ID = "raspi-001"
STATUS_TOPIC = "home_status"
DHT_PIN = 4  # GPIO για αισθητήρα DHT22

# Ρύθμιση MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_BROKER, 1883, 60)
client.loop_start()

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT_PIN)
        if humidity is not None and temperature is not None:
            payload = {
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2),
                "unit": "°C",
                "device_id": DEVICE_ID
            }
            client.publish(STATUS_TOPIC, json.dumps(payload))
            print("Αποστολή μετρήσεων MQTT:", payload)
        else:
            print("Αποτυχία ανάγνωσης από τον αισθητήρα DHT22.")
        time.sleep(2)

except KeyboardInterrupt:
    print("Τερματισμός publisher από τον χρήστη.")
    client.loop_stop()

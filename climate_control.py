import paho.mqtt.client as mqtt
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import json

# CONFIG
MQTT_BROKER = "192.168.1.2"  # Windows IP που τρέχει το Mosquitto
DEVICE_ID = "raspi-001"

STATUS_TOPIC = "home_status"
COMMAND_TOPIC = "hvac_status"

# GPIO PINS
DHT_PIN = 4
RELAY_HEAT = 5
RELAY_COOL = 6
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

# MODE = "heat" ή "cool" ή "idle"
mode = "idle"

# SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_HEAT, GPIO.OUT)
GPIO.setup(RELAY_COOL, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

GPIO.output(RELAY_HEAT, GPIO.LOW)
GPIO.output(RELAY_COOL, GPIO.LOW)

# LED HELPERS
def set_rgb(r, g, b):
    GPIO.output(RED_PIN, not r)
    GPIO.output(GREEN_PIN, not g)
    GPIO.output(BLUE_PIN, not b)

# CLIMATE CONTROL HELPERS
def heat_on():
    GPIO.output(RELAY_HEAT, GPIO.HIGH)
    GPIO.output(RELAY_COOL, GPIO.LOW) 

def cool_on():
    GPIO.output(RELAY_HEAT, GPIO.LOW)
    GPIO.output(RELAY_COOL, GPIO.HIGH) 

def climate_off():
    GPIO.output(RELAY_HEAT, GPIO.LOW)
    GPIO.output(RELAY_COOL, GPIO.LOW) 




# MQTT CALLBACKS
def on_connect(client, userdata, flags, rc, properties=None):
    print("Σύνδεση στον broker")
    client.subscribe(COMMAND_TOPIC)
    
def on_message(client, userdata, msg):
    try:
        command = msg.payload.decode().strip().upper()
        print(f"Received command: {command}")

        if command == "HEAT_ON":
            heat_on()
            set_rgb(1, 0, 0)

        elif command == "HEAT_OFF":
            climate_off()
            set_rgb(0, 1, 0)

        elif command == "COOL_ON":
            cool_on()
            set_rgb(0, 0, 1)

        elif command == "COOL_OFF":
            climate_off()
            set_rgb(0, 1, 0)

        elif command == "IDLE":
            climate_off()
            set_rgb(0, 1, 0)

        else:
            print("Unknown command")

    except Exception as e:
        print("Error in message:", e)


# MQTT SETUP
try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()



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
            print("Published:", payload)
        else:
            print("failed to recieve DHT22")
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
    client.loop_stop()
except Exception as e:
    print(f"Error during MQTT setup or loop: {e}")
    GPIO.cleanup()
    client.loop_stop()

finally:
    print("Cleaning up GPIO and stopping MQTT")
    GPIO.cleanup()
    try:
        client.loop_stop()
    except:
        pass  # in case client creation failed

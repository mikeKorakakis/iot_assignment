import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# ΡΥΘΜΙΣΕΙΣ
MQTT_BROKER = "192.168.1.2"
COMMAND_TOPIC = "hvac_status"
RELAY_HEAT = 5
RELAY_COOL = 6
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

# Ρύθμιση GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_HEAT, GPIO.OUT)
GPIO.setup(RELAY_COOL, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)
GPIO.output(RELAY_HEAT, GPIO.LOW)
GPIO.output(RELAY_COOL, GPIO.LOW)

# LED: Αντιστοίχιση χρωμάτων
def set_rgb(r, g, b):
    GPIO.output(RED_PIN, not r)
    GPIO.output(GREEN_PIN, not g)
    GPIO.output(BLUE_PIN, not b)

# Έλεγχος ρελέ
def heat_on():
    GPIO.output(RELAY_HEAT, GPIO.HIGH)
    GPIO.output(RELAY_COOL, GPIO.LOW)

def cool_on():
    GPIO.output(RELAY_HEAT, GPIO.LOW)
    GPIO.output(RELAY_COOL, GPIO.HIGH)

def climate_off():
    GPIO.output(RELAY_HEAT, GPIO.LOW)
    GPIO.output(RELAY_COOL, GPIO.LOW)

# MQTT callbacks
def on_connect(client, userdata, flags, rc, properties=None):
    print("Συνδέθηκε με τον MQTT Broker.")
    client.subscribe(COMMAND_TOPIC)

def on_message(client, userdata, msg):
    try:
        command = msg.payload.decode().strip().upper()
        print(f"Ελήφθη εντολή: {command}")

        if command == "HEAT_ON":
            heat_on()
            set_rgb(1, 0, 0)
            print("Ενεργοποιήθηκε η Θέρμανση.")

        elif command == "HEAT_OFF":
            climate_off()
            set_rgb(0, 1, 0)
            print("Απενεργοποιήθηκε η Θέρμανση.")

        elif command == "COOL_ON":
            cool_on()
            set_rgb(0, 0, 1)
            print("Ενεργοποιήθηκε η Ψύξη.")

        elif command == "COOL_OFF":
            climate_off()
            set_rgb(0, 1, 0)
            print("Απενεργοποιήθηκε η Ψύξη.")

        elif command == "IDLE":
            climate_off()
            set_rgb(0, 1, 0)
            print("Λειτουργία σε Αναμονή.")

        else:
            print("Άγνωστη εντολή.")

    except Exception as e:
        print("Σφάλμα κατά την επεξεργασία εντολής:", e)

# Εκκίνηση MQTT client
try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()

except KeyboardInterrupt:
    print("Τερματισμός subscriber από τον χρήστη.")
    GPIO.cleanup()
except Exception as e:
    print("Σφάλμα στον subscriber:", e)
    GPIO.cleanup()
finally:
    GPIO.cleanup()

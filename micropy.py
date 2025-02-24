import network
import time
import urequests
import dht
from machine import Pin, ADC
from config import CONFIG

# Konfigurasi WiFi
SSID = CONFIG["WIFI_SSID"]
PASSWORD = CONFIG["WIFI_PASSWORD"]

# Konfigurasi Ubidots
UBIDOTS_TOKEN = CONFIG["UBIDOTS_TOKEN"]
UBIDOTS_URL = CONFIG["UBIDOTS_URL"]

# Konfigurasi MongoDB Server Flask
MONGO_SERVER_URL = CONFIG["MONGO_SERVER_URL"]

# Inisialisasi Sensor
dht_pin = Pin(4)
dht_sensor = dht.DHT11(dht_pin)
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)

# Koneksi WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Menghubungkan ke WiFi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print("Terhubung ke WiFi:", wlan.ifconfig())

# Kirim data ke Ubidots
def send_to_ubidots(temp, hum, light):
    headers = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}
    data = {"temperature": temp, "humidity": hum, "light": light}
    
    try:
        response = urequests.post(UBIDOTS_URL, json=data, headers=headers)
        print("Data ke Ubidots:", response.text)
        response.close()
    except Exception as e:
        print("Gagal kirim ke Ubidots:", e)

# Kirim data ke MongoDB
def send_to_mongo(temp, hum, light):
    data = {"temperature": temp, "humidity": hum, "light": light}
    
    try:
        response = urequests.post(MONGO_SERVER_URL, json=data, headers={"Content-Type": "application/json"})
        print("Data ke MongoDB:", response.text)
        response.close()
    except Exception as e:
        print("Gagal kirim ke MongoDB:", e)

connect_wifi()

while True:
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        light_intensity = ldr.read()

        print(f"Temp: {temperature}°C, Humidity: {humidity}%, Light: {light_intensity}")

        send_to_ubidots(temperature, humidity, light_intensity)
        send_to_mongo(temperature, humidity, light_intensity)

    except Exception as e:
        print("Error:", e)

    time.sleep(10)
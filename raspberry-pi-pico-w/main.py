import network
import socket
import json
from machine import Pin
import time
from secrets import WIFI_SSID, WIFI_PASSWORD


# GPIO pin for the On Air indicator (using built-in LED for testing)
ON_AIR_PIN = 16  # GPIO16 pin
on_air_status = False

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print('Connected to WiFi')
    print('Network config:', wlan.ifconfig())

def setup_gpio():
    if ON_AIR_PIN == "LED":
        pin = Pin("LED", Pin.OUT)
    else:
        pin = Pin(int(ON_AIR_PIN), Pin.OUT)
    return pin

def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print('Received request:', request)
    
    # Parse the request
    try:
        # Extract the JSON data from the request
        json_start = request.find('{')
        if json_start == -1:
            response = 'HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid request format'
            client_socket.send(response.encode())
            return
        
        json_data = request[json_start:]
        data = json.loads(json_data)
        
        # Check if the request contains the on_air field
        if 'on_air' not in data:
            response = 'HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nMissing on_air field'
            client_socket.send(response.encode())
            return
        
        # Update the on_air status
        global on_air_status
        on_air_status = data['on_air']
        
        # Update the GPIO pin
        led.value(1 if on_air_status else 0)
        
        # Send response
        response_data = {'status': 'success', 'on_air': on_air_status}
        response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n' + json.dumps(response_data)
        client_socket.send(response.encode())
        
    except json.JSONDecodeError:
        response = 'HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid JSON'
        client_socket.send(response.encode())
    except Exception as e:
        response = 'HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\n' + str(e)
        client_socket.send(response.encode())

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 80))
    server.listen(1)
    print('Server started on port 80')
    
    while True:
        client_socket, addr = server.accept()
        print('Client connected from:', addr)
        handle_request(client_socket)
        client_socket.close()

# Initialize GPIO
led = setup_gpio()

# Connect to WiFi
connect_to_wifi()

# Start the server
start_server() 
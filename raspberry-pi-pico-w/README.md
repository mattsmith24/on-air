# Raspberry Pi Pico W On Air Controller

This project implements a simple REST API on a Raspberry Pi Pico W that controls
an "On Air" status indicator using a GPIO pin.

## Features

- WiFi connectivity
- REST API endpoint for controlling On Air status
- GPIO control for visual indicator
- JSON-based communication

## Setup

1. Flash MicroPython to your Raspberry Pi Pico W
   - Download the latest MicroPython firmware from
     [micropython.org](https://micropython.org/download/RPI_PICO_W/)
   - Hold the BOOTSEL button while connecting the Pico W to your computer
   - Copy the firmware file to the Pico W

2. Configure WiFi
   - Create a file  `secrets.py` and add WiFi credentials:
     ```python
     WIFI_SSID = "YOUR_WIFI_SSID"
     WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
     ```

3. Configure GPIO
   - By default, the script uses the built-in LED for testing
   - To use a different GPIO pin, change the `ON_AIR_PIN` variable to the
     desired pin number

4. Upload the code
   - Copy `main.py` to your Pico W
   - The device will automatically connect to WiFi and start the server

## Usage

Send a POST request to the Pico W's IP address (port 80) with a JSON body:

```json
{
    "on_air": true
}
```

or

```json
{
    "on_air": false
}
```

The server will respond with:

```json
{
    "status": "success",
    "on_air": true
}
```

## Testing

You can test the API using curl:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"on_air":true}' http://<pico-ip-address>
```

## Troubleshooting

1. If the device doesn't connect to WiFi:
   - Check your WiFi credentials
   - Ensure you're using 2.4GHz WiFi (Pico W doesn't support 5GHz)
   - Check the serial console for error messages

2. If the API doesn't respond:
   - Verify the Pico W's IP address from the serial console
   - Ensure no firewall is blocking port 80
   - Check the serial console for any error messages 
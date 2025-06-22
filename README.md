This project is a simple solution to control an "On Air" sign using a Raspberry
Pi and a GPIO pin.

The on-air shell script is used to monitor the state of the /dev/video0 device
using lsof. If the device is in use, then a call is made to a REST API on the
rasberry pi to notify that the video device is active.

The on-air-api.py is a Flask application that provides a REST API to control the
GPIO pin. A simple POST request can control the state of the GPIO pin. The API
also provides a GET request to retrieve the current state of the GPIO pin.

Example POST request body to turn the GPIO pin on:

``` json
{
    "state": 1
}
```

## Installation

### On Raspberry Pi

1. Install required packages:
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-flask python3-rpi.gpio
pip3 install flask
```

2. Copy the service files to systemd:
```bash
sudo cp on-air-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable on-air-api
sudo systemctl start on-air-api
```

3. Verify the service is running:
```bash
sudo systemctl status on-air-api
```

### On Laptop

1. Copy the service files to systemd:
```bash
sudo cp on-air.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable on-air
sudo systemctl start on-air
```

2. Verify the service is running:
```bash
sudo systemctl status on-air
```

## Configuration

Edit the `API_HOST` variable in the `on-air` script to match your Raspberry Pi's hostname or IP address.

## Troubleshooting

Check service logs:
```bash
# On Raspberry Pi
journalctl -u on-air-api -f

# On Laptop
journalctl -u on-air -f
```

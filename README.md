This project is a simple solution to control an "On Air" sign using a Raspberry
Pi Pico W GPIO pin. The use case is where you want to notify people around you
that you are recording video or in an online meeting.

It is designed for a Linux or macOS PC/laptop and uses Raspberry Pi Pico W (or
similar) to host an API connected to a GPIO pin which controls the driver
circuit for the sign.

The `on-air` shell script monitors camera activity and calls a REST API on the
Raspberry Pi when the camera state changes.
- Linux: checks if `/dev/video0` (configurable via `VIDEO_DEVICE`) is in use.
- macOS: checks Apple camera in-use clients via `ioreg`
  (`AppleH16CamInUserClient` / `AppleH13CamInUserClient`) and matches
  `IOUserClientCreator` with `cameracaptured`, then falls back to generic
  `ioreg` in-use flags and legacy camera assistants.

The main script on the raspberry pi provides a REST API to control the GPIO pin.
A simple POST request can control the state of the GPIO pin.

Example POST request body to turn the GPIO pin on:

``` json
{
    "on_air": true
}
```

# Installation On Linux Laptop / PC

Adjust the path to the on-air script in the service file. It assumes
/opt/on-air.

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

# Installation On macOS

Adjust the path in `on-air.plist` if your script is not in `/opt/on-air/on-air`.

1. Copy the launch agent:
```bash
mkdir -p ~/Library/LaunchAgents
cp on-air.plist ~/Library/LaunchAgents/com.onair.sign.plist
launchctl load -w ~/Library/LaunchAgents/com.onair.sign.plist
```

2. Verify it is loaded:
```bash
launchctl list | grep com.onair.sign
```

## Configuration

Edit the `API_HOST` variable in the `on-air` script to match your Raspberry Pi's hostname or IP address.
For Linux, you can also set `VIDEO_DEVICE` if your camera is not `/dev/video0`.

## Troubleshooting

Check service logs:
```bash
# On Laptop
journalctl -u on-air -f
```

```bash
# On macOS
tail -f /tmp/on-air.log /tmp/on-air.err
```

# Raspberry Pi Pico W On Air Controller

This project implements a simple REST API on a Raspberry Pi Pico W that controls
an "On Air" status indicator using a GPIO pin.

## Features

- WiFi connectivity
- REST API endpoint for controlling On Air status
- GPIO control for visual indicator
- JSON-based communication

## Setup

It will help to read the online getting started guide first.
https://projects.raspberrypi.org/en/projects/get-started-pico-w

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

# Hardware

A USB powered on-air sign like this one on Amazon
https://www.amazon.com.au/NPW-Gifts-Retro-Light-Board/dp/B0BHL1S1TC. Any sign or
lamp that is powered by a USB port will do.

Some electronic bits:

- Veroboard or breadboard big enough for the Rasberry Pi and the MOSFET. Mine is
  25 x 16 holes and there was plenty of room.
- Raspberry Pi Pico W
- A MOSFET that will fully switch on at 3.3V such as IRLB8721. Don't use the
  more common 5V ones that are used with Arduinos.
- 10kOhm resistor
- Tinned copper wire about 0.71mm diameter (just for hooking up the circuit)

Tools

- Wire strippers
- Solder and resin
- Soldering iron
- Micro-USB cable with data suitable for programming the Pico W

Refer to the diagram in on-air-circuit-diagram.svg and create a similar diagram using veroboard
or breadboard.

Cut the USB cable and use wire strippers to expose the cores. The USB cable that
came with my sign had one red core for 5V and the black for ground. Solder the
USB-A side to the +5V and GND rails of your circuit. On the micro-usb side for
powering the light, connect to +5V and the Drain pin on the MOSFET.

![On-Air Circuit Diagram](on-air-circuit-diagram.svg)

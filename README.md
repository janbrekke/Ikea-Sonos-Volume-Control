# Ikea Sonos Volume Controller
A simple Python script to control the volume of Sonos-based speakers (including IKEA Symfonisk) over the local network using their UPnP/SOAP API.

## Features
* View current volume
* Increase / decrease volume by +5 or -5 (No slider yet maybe i'll add it later)
* Set volume manually (0–100)
* Direct control via local IP (no cloud required)

## How It Works
Sonos speakers expose a local control interface over HTTP (port 1400) using the UPnP protocol.

This script sends SOAP requests directly to the speaker to:

* Retrieve current volume
* Adjust volume in real-time

No authentication is required as long as you're on the same local network as the speaker.

## Requirements
* Python 3.8+
* request library

Install the dependencies using:

***pip install requests***

## Usage
1. Clone the repository:
2. git clone https://github.com/janbrekke/Ikea-Sonos-Volume-Control.git
3. cd sonos-volume-controller
4. Edit the script and set your speaker IP:
speaker = SonosSpeaker("192.168.1.50")
5. Run the application:
python sonos-volume-controller.py

## FYI
* The speaker must be on the same local network for it to work (guess you figured this one out)
* Port 1400 must be reachable over the network. Firewall or network routing must not block this 🙃
* Volume range is limited to 0–100, you know; just to not make it more difficult than it has to be. I could always set 32 as 1% and 87 as 100% but hey, I'm not evil.
* Rapid repeated calls to the speaker may cause the script to lag or stop responding. In other words; don't spam the buttons like a teenager in 2026 waiting for a Commodore64 tape player to finish loading the game.

## Future ideas
* Volume slider (Shouldn't be to hard)
* Multi-speaker support (Can't be hard either)
* Auto-discover Sonos devices on network (this would be handy)
* Home Assistant integration? Naah? Maybe? Dunno..

### Have fun..

import tkinter as tk
from tkinter import ttk, messagebox
import requests
from xml.etree import ElementTree as ET


class SonosSpeaker:
    def __init__(self, ip: str, timeout: float = 3.0):
        self.ip = ip
        self.timeout = timeout
        self.url = f"http://{ip}:1400/MediaRenderer/RenderingControl/Control"

    def _send_soap(self, action: str, body_xml: str) -> str:
        headers = {
            "Content-Type": 'text/xml; charset="utf-8"',
            "SOAPACTION": f'"urn:schemas-upnp-org:service:RenderingControl:1#{action}"',
        }

        envelope = f"""<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
            s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    {body_xml}
  </s:Body>
</s:Envelope>"""

        response = requests.post(
            self.url,
            data=envelope.encode("utf-8"),
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.text

    def get_volume(self) -> int:
        body = """
<u:GetVolume xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1">
  <InstanceID>0</InstanceID>
  <Channel>Master</Channel>
</u:GetVolume>
"""
        xml_text = self._send_soap("GetVolume", body)

        root = ET.fromstring(xml_text)
        for elem in root.iter():
            if elem.tag.endswith("CurrentVolume"):
                return int(elem.text)

        raise RuntimeError("Could not get volume from Sonos response.")

    def set_volume(self, volume: int) -> None:
        volume = max(0, min(100, int(volume)))

        body = f"""
<u:SetVolume xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1">
  <InstanceID>0</InstanceID>
  <Channel>Master</Channel>
  <DesiredVolume>{volume}</DesiredVolume>
</u:SetVolume>
"""
        self._send_soap("SetVolume", body)

    def volume_up(self, step: int = 5) -> int:
        current = self.get_volume()
        new_volume = min(100, current + step)
        self.set_volume(new_volume)
        return new_volume

    def volume_down(self, step: int = 5) -> int:
        current = self.get_volume()
        new_volume = max(0, current - step)
        self.set_volume(new_volume)
        return new_volume


# Change the IP address to match your Sonos IP
speaker = SonosSpeaker("192.168.0.179")


def refresh_volume():
    try:
        vol = speaker.get_volume()
        volume_label.config(text=f"Volume: {vol}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not get volume:\n{e}")


def on_up():
    try:
        new_vol = speaker.volume_up(5)
        volume_label.config(text=f"Volume: {new_vol}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not raise volume:\n{e}")


def on_down():
    try:
        new_vol = speaker.volume_down(5)
        volume_label.config(text=f"Volume: {new_vol}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not lower volume:\n{e}")


def on_set():
    try:
        vol = int(volume_entry.get())
        speaker.set_volume(vol)
        volume_label.config(text=f"Volume: {speaker.get_volume()}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a number from 0 to 100.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not set volume:\n{e}")


# GUI window settings
root = tk.Tk()
root.title("Sonos Volume Control")
root.geometry("300x240")

title_label = ttk.Label(root, text="Sonos / IKEA Speaker Control", font=("Arial", 11, "bold"))
title_label.pack(pady=10)

volume_label = ttk.Label(root, text="Volume: ?", font=("Arial", 10))
volume_label.pack(pady=10)

button_frame = ttk.Frame(root)
button_frame.pack(pady=5)

down_button = ttk.Button(button_frame, text="Volume -", command=on_down)
down_button.grid(row=0, column=0, padx=5)

up_button = ttk.Button(button_frame, text="Volume +", command=on_up)
up_button.grid(row=0, column=1, padx=5)

volume_entry = ttk.Entry(root, width=10)
volume_entry.pack(pady=8)

set_button = ttk.Button(root, text="Set Volume", command=on_set)
set_button.pack(pady=5)

# The REFRESH button is just to update the script with the current volume.
# If the volume is changed by another device the script won't auto update.
# It's not important, but it's just to see the current volume status of the Sonos device.
refresh_button = ttk.Button(root, text="Refresh", command=refresh_volume)
refresh_button.pack(pady=5)

refresh_volume()
root.mainloop()
# Flock 🕊️

Utilities for a hacked Flock camera.

The current implementation involves:
- A Raspberry Pi 4b.
- A IMX477 Flock camera sensor.
- A separate computer to view the video stream.

The Pi connects to the sensor, runs `flock_stream.service` and produces a video stream that is viewable in a web browser at `http://<your_ip_addr>:8888/cam/`.

An optional client computer displays video in a fullscreen firefox browser (kiosk mode) by running `flock_display.service`. This is tested on a Ubuntu desktop.

I strongly recommend running everything behind a *Tailscale VPN* if internet access is available.


## Setup

Set up the repo:
- `git clone `
- `python3 -m venv .venv --system-site-packages` (for pi cam library)

Enable the camera module [link](https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/12MP-IMX477/#raspberry-pi-5-cm5). 

Edit the config:
- `sudo vim /boot/firmware/config.txt`

And change:
- `camera_auto_detect=0`.

Under the `[all]` section add:
- `dtoverlay=imx477`.

Then `sudo reboot`.

Test it out: 
- `rpicam-still -o test.jpg`

Install mediamtx server to handle RTSP stream:
- `cd /tmp`
- `wget https://github.com/bluenviron/mediamtx/releases/download/v1.21.2/mediamtx_v1.21.2_linux_arm64.tar.gz`
- `tar -xzf mediamtx_v1.21.2_linux_arm64.tar.gz`
- `sudo install mediamtx /usr/local/bin/mediamtx`
- `sudo mkdir -p /usr/local/etc`

Create a *mediamtx* config `sudo vim /usr/local/etc/mediamtx.yml` with the following contents: 

```
logLevel: info
rtsp: true
rtspAddress: :8554
hls: true
hlsAddress: :8888
hlsAllowOrigins: ['*']

paths:
  cam:
    source: publisher
```

Then create a *systemd* service: `sudo vim /etc/systemd/system/mediamtx.service`

```
[Unit]
Description=MediaMTX
After=network.target

[Service]
ExecStart=/usr/local/bin/mediamtx /usr/local/etc/mediamtx.yml
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Then start and enable the service:
- `sudo systemctl daemon-reload`
- `sudo systemctl enable --now mediamtx`
- `sudo systemctl status mediamtx`

**NOTE**: no third party packages are imported so a virtual environment is not required.


## Test

- `python flock_stream.py`

Then view the feed locally in a browser at `http://127.0.0.1:8888/cam/` or from another computer at `http://<ip address>:8888/cam/`

Or view it in vlc with:
- `vlc --rtsp-tcp "rtsp://<ip address>:8554/cam"`


## Run in production

On the Raspberry Pi connected to the Flock sensor, set up a *systemd* service to run the server at startup:
- `mkdir -p ~/.config/systemd/user`
- `cat flock_stream.service > ~/.config/systemd/user/flock_stream.service`

Start the service using the commands below:
- `systemctl --user daemon-reload`
- `systemctl --user enable flock_stream.service`
- `systemctl --user start flock_stream.service`

Start it on boot:
- `sudo loginctl enable-linger $(whoami)`

Get the logs:
- `journalctl --user -u flock_stream.service`

On the optional second machine running Ubuntu, set up the video viewer. **NOTE**: the Raspberry pi that captures the video stream from the Flock sensor and the computer that displays the video stream (if different computers) must be on the same LAN or VPN. Also **NOTE** that this code can easily be adapted for a machine running MacOS, Windows, or Raspbian.

View from any machine with:
- `DISPLAY=:0 firefox --kiosk --new-window http://<ip address>:8888/cam/`

Then continue with:
- `cat flock_display.service > ~/.config/systemd/user/flock_display.service`
- `systemctl --user daemon-reload`
- `systemctl --user enable flock_display.service`
- `systemctl --user start flock_display.service`

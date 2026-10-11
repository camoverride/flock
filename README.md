# Flock

Utilities for a hacked Flock camera.


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


## Test

- `python flock_stream.py`

Then view the feed locally in a browser at `http://127.0.0.1:8888/cam/` or from another computer at `http://<ip address>:8888/cam/`

Or view it in vlc with:

- `vlc --rtsp-tcp "rtsp://<ip address>:8554/cam"`


## Run in production

Set up a *systemd* service to run the server at startup:

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

View from any machine with:

- `DISPLAY=:0 firefox --kiosk --new-window http://<ip address>:8888/cam/`

Then continue with:

- `cat flock_display.service > ~/.config/systemd/user/flock_display.service`
- `systemctl --user daemon-reload`
- `systemctl --user enable flock_display.service`
- `systemctl --user start flock_display.service`

import logging
import os
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import PyavOutput



URL = f"rtsp://100.116.247.74:8554/cam"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("camera")


def record():
    camera = Picamera2()
    recording = False

    try:
        config = camera.create_video_configuration(
            main={"size": (1920, 1080), "format": "YUV420"},
            controls={"FrameRate": 30})

        camera.configure(config)

        encoder = H264Encoder(bitrate=4_000_000)
        output = PyavOutput(URL, format="rtsp")

        log.info("Streaming camera to %s", URL)
        camera.start_recording(encoder, output)
        recording = True

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        log.info("Stopping stream")

    finally:
        if recording:
            camera.stop_recording()
        camera.close()



if __name__ == "__main__":
    record()

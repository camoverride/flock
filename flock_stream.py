import logging
import time
from picamera2 import Picamera2             # type: ignore
from picamera2.encoders import H264Encoder  # type: ignore
from picamera2.outputs import PyavOutput    # type: ignore



# Serve locally.
URL = f"rtsp://127.0.0.1:8888/cam"

# Set up logging.
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("camera")


def record():
    """
    Sends RTSP to the designated server.
    """
    camera = Picamera2()
    recording = False

    try:
        # Camera configuration.
        # NOTE: requires these parameters under "main"
        # otherwise the top and bottom of the frame are cut off.
        config = camera.create_video_configuration(
            main={"size": (1440, 1080), "format": "YUV420"},
            raw={"size": (2028, 1520)},
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

from gpiozero import Button, LED, DigitalInputDevice  # type: ignore
from signal import pause
import subprocess
import atexit



led = LED(17)
button = Button(26, pull_up=True)
motion = DigitalInputDevice(21, pull_up=False)
silent = True
AUDIO_FILE = "audio/alert.mp3"


def handle_motion():
    """
    Turn on LEDs, play sound, then turn off LEDs.
    """
    led.on()

    try:
        if not silent:
            subprocess.run([
                "ffplay", "-nodisp", "-autoexit",
                "-loglevel", "quiet", AUDIO_FILE])

    finally:
        led.off()


def toggle_mode():
    """
    Toggle audio on or off.
    """
    global silent
    silent = not silent
    print("Silent" if silent else "Audio enabled")


atexit.register(led.off)
motion.when_activated = handle_motion
button.when_pressed = toggle_mode

try:
    pause()
finally:
    led.off()

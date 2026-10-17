
from gpiozero import Button, LED, DigitalInputDevice
from signal import pause, SIGINT, SIGTERM
import subprocess
import atexit



BUTTON_PIN = 26
MOTION_PIN = 21
LED_PIN = 17
AUDIO_FILE = "/home/pi/sounds/alert.mp3"

silent = True
busy = False

led = LED(LED_PIN)
button = Button(BUTTON_PIN, pull_up=True)
motion = DigitalInputDevice(MOTION_PIN, pull_up=False)


def play_audio():
    """
    Play the MP3 (blocking)
    """
    if not silent:
        subprocess.run([
            "ffplay", "-nodisp", "-autoexit",
            "-loglevel", "quiet", AUDIO_FILE
        ], check=False)


def handle_motion():
    """
    Turn on LEDs, play audio, then turn LEDs off.
    """
    global busy

    if busy:
        return

    busy = True
    try:
        led.on()
        play_audio()
    finally:
        led.off()
        busy = False


def toggle_mode():
    """
    Toggle between silent and audio-enabled modes.
    """
    global silent
    silent = not silent
    print("Silent mode" if silent else "Audio mode enabled")


def cleanup():
    """
    Ensure LEDs are off when the program exits.
    """
    led.off()


button.when_pressed = toggle_mode
motion.when_activated = handle_motion

atexit.register(cleanup)

print("System ready — silent mode")

try:
    pause()
finally:
    cleanup()

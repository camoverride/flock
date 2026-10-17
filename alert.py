from gpiozero import Button, LED, DigitalInputDevice # type: ignore
from signal import pause
from threading import Timer
import subprocess



BUTTON_PIN = 26
MOTION_PIN = 21
LED_PIN = 17
AUDIO_FILE = "audio/obey.mp3"

silent = False
led_timer = None
audio_process = None

led = LED(LED_PIN)
button = Button(BUTTON_PIN, pull_up=True)
motion = DigitalInputDevice(MOTION_PIN, pull_up=False)


def play_audio():
    """
    Play the MP3 and wait for playback to finish.
    """
    if not silent:
        subprocess.run([
            "ffplay", "-nodisp", "-autoexit",
            "-loglevel", "quiet", AUDIO_FILE
        ], check=False)


def turn_off_leds():
    """
    Turn off LEDs after the motion timeout.
    """
    led.off()


def handle_motion():
    """
    Keep LEDs on for five seconds after the latest motion.
    """
    global led_timer

    led.on()

    if led_timer is not None:
        led_timer.cancel()

    led_timer = Timer(5, turn_off_leds)
    led_timer.start()

    play_audio()


def toggle_mode():
    """
    Switch between silent and audio-enabled modes.
    """
    global silent

    silent = not silent
    print("Silent mode" if silent else "Audio mode enabled")


button.when_pressed = toggle_mode
motion.when_activated = handle_motion

print("System ready!")
pause()

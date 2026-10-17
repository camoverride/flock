from gpiozero import Button, LED, DigitalInputDevice  # type: ignore
import pygame  # type: ignore
from threading import Thread
from time import sleep



button = Button(26, pull_up=True)
motion = DigitalInputDevice(21, pull_up=False)
leds = LED(17)

sound_on = True

pygame.mixer.init()
pygame.mixer.music.load("audio/obey.mp3")



def wait_for_button():
    global sound_on
    while True:
        button.wait_for_press()
        sound_on = not sound_on
        print("Sound on" if sound_on else "Sound off")
        button.wait_for_release()

Thread(
    target=wait_for_button,
    daemon=True).start()

while True:
    if motion.value:
        # Turn on the LEDs if there's motion
        leds.on()

        # If audio is enabled, play it.
        if sound_on:
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                sleep(0.1)
        # Otherwise keep the LEDs on for 5 seconds.
        else:
            sleep(5)

        leds.off()
        sleep(1)
    else:
        sleep(1)

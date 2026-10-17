from gpiozero import Button   # type: ignore
from signal import pause



button = Button(26, pull_up=True)

button.when_pressed = lambda: print("Button pressed")
button.when_released = lambda: print("Button released")

pause()

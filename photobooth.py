from time import sleep
import RPi.GPIO as GPIO

# config
button_delay = 0.1
button_pin = 12
button_led_pin = 11
smile_led_pin = 16

class Camera:
    camera_available = True

    def set_state(self,newState):
        self.camera_available = newState

def button_pressed():
    return (GPIO.input(button_pin) == False)

def turn_button_led_off():
    print("button led off")
    GPIO.output(button_led_pin, GPIO.LOW)

def turn_button_led_on():
    print("button led on")
    GPIO.output(button_led_pin, GPIO.HIGH)

def turn_smile_led_off():
    print("smile led off")
    GPIO.output(smile_led_pin, GPIO.LOW)

def turn_smile_led_on():
    print("smile led on")
    GPIO.output(smile_led_pin, GPIO.HIGH)

def button_loop(cam):  

    i = 0

    while 1:

        if button_pressed() and cam.camera_available:
            turn_button_led_off()
            start_photo_seq(cam)
        elif i == 8:
            turn_button_led_on()
        elif i == 16:
            turn_button_led_off()
            i = 0

        sleep(button_delay)        
        i += 1


def start_photo_seq(cam):
    cam.set_state(False)
    turn_smile_led_on()
    print("cheeeeese :)")
    sleep(10)
    print("ready")
    cam.set_state(True)
    turn_smile_led_off()

def setup_gpio():

    GPIO.setmode(GPIO.BOARD)

    # led
    GPIO.setup(smile_led_pin, GPIO.OUT)
    GPIO.output(smile_led_pin, GPIO.HIGH)
    GPIO.setup(button_led_pin, GPIO.OUT)
    GPIO.output(button_led_pin, GPIO.HIGH)

    # button
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if __name__ == '__main__':

    setup_gpio()
    cam = Camera()
    button_loop(cam)
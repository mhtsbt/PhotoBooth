import time
import RPi.GPIO as GPIO
import pygame
import pygame.camera
from fpdf import FPDF
import subprocess

# config
button_delay = 0.1
button_pin = 12
button_led_pin = 11
smile_led_pin = 16

# camera setup
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))

def button_pressed():
    return (GPIO.input(button_pin) == False)

def turn_button_led_off():
    GPIO.output(button_led_pin, GPIO.LOW)

def turn_button_led_on():
    GPIO.output(button_led_pin, GPIO.HIGH)

def turn_smile_led_off():
    GPIO.output(smile_led_pin, GPIO.LOW)

def turn_smile_led_on():
    GPIO.output(smile_led_pin, GPIO.HIGH)

def button_loop():  

    i = 0

    while 1:

        if button_pressed():            
            start_photo_seq()
        elif i == 8:
            turn_button_led_on()
        elif i == 16:
            turn_button_led_off()
            i = 0

        time.sleep(button_delay)        
        i += 1


def start_photo_seq():
    turn_button_led_off()
    turn_smile_led_on()

    filename = str(time.time()).split('.')[0]

    print(filename)

    print("cheeeeese :)")
    time.sleep(1)
    take_picture(filename)
    print_picture(filename)
    print("ready")
    turn_smile_led_off()
    return

def setup_gpio():

    GPIO.setmode(GPIO.BOARD)

    # led
    GPIO.setup(smile_led_pin, GPIO.OUT)
    GPIO.setup(button_led_pin, GPIO.OUT)

    # button
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def destory_gpio():
    turn_button_led_off()
    turn_smile_led_off()
    GPIO.cleanup()
    print("cleanup finished")

def take_picture(filename):
    cam.start()
    img = cam.get_image()
    filename = '/home/pi/pics/'+filename+'.jpg'
    pygame.image.save(img, filename)

def generate_pdf(filename):

    pic = '/home/pi/pics/'+filename+'.jpg'
    out_file = '/home/pi/pics/'+filename+'.pdf'

    pdf = FPDF('P', 'mm', (100, 150))
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 5, 'MATTHIAS & CELINE')
    pdf.image(name=pic, x =5, y = 20, w = 90, h = 70, link = pic)

    pdf.output(out_file, 'F')

    print("pdf ready")

def print_picture(filename):

    print("printing")
    generate_pdf(filename)

    full_path = '/home/pi/pics/'+filename+'.pdf'
    print(full_path)
    print (subprocess.check_output(['lp',full_path]))

if __name__ == '__main__':

    try:        
        setup_gpio()
        button_loop()
    finally:
        destory_gpio()

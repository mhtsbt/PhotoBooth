<<<<<<< HEAD
#!/usr/bin/env python3

=======
import os
>>>>>>> 936f52ec01fc47a6e574551ee5e355bc5600f7d2
import time
import RPi.GPIO as GPIO
import pygame
import pygame.camera
from fpdf import FPDF
from pypdf import PdfReader, PdfWriter
import subprocess
<<<<<<< HEAD
from PIL import Image 
import board
import neopixel

=======
from PIL import Image
>>>>>>> 936f52ec01fc47a6e574551ee5e355bc5600f7d2

# config
button_delay = 0.1
button_pin = 14
button_led_pin = 11
smile_led_pin = 16
enable_print = True
pictures_location = "/home/photobooth/Pictures"
background_pdf_path = f"{pictures_location}/background.pdf"

pixels = neopixel.NeoPixel(board.D18, 24)
pixels.fill((0, 255, 0))

#subprocess.run(["amixer","set","PCM","--","100%"])


# camera setup
pygame.init()

pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))

#pygame.mixer.init()

def button_pressed():
    return (GPIO.input(button_pin) == 0)

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

    while True:
#        print("waiting")
        if button_pressed():
             try:
                 start_photo_seq()
             except Exception as e:
                 print(e)
        time.sleep(button_delay)        

def start_photo_seq():
   # turn_button_led_off()
   # turn_smile_led_on()

    #pygame.mixer.music.load("/home/pi/photobooth/countdown.mp3")
   # pygame.mixer.music.play()
   # pygame.event.wait()


    filename = str(time.time()).split('.')[0]

    print(filename)

    pixels.fill((255, 0, 0))
    print("cheeeeese :)")
    time.sleep(6)
    pixels.fill((255, 255, 255))

    print("Taking picture")
    take_picture(filename)

    if enable_print:
        print_picture(filename)
    print("ready")
    pixels.fill((0, 0, 0))
 #   turn_smile_led_off()
    return

def setup_gpio():

    GPIO.setmode(GPIO.BCM)

    # button
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def destory_gpio():
#    turn_button_led_off()
#    turn_smile_led_off()
    GPIO.cleanup()
    print("cleanup finished")

def take_picture(filename):
    cam.start()
    img = cam.get_image()
    filename = f'{pictures_location}/{filename}.jpg'

    data = pygame.image.tostring(img, 'RGB')
    pil_img = Image.frombytes('RGB', img.get_size(), data)
    pil_img.save(filename)

    #pygame.image.save(img, filename)
    cam.stop()

def generate_pdf(filename):

    pic = f'{pictures_location}/'+filename+'.jpg'
    out_file = f'{pictures_location}/'+filename+'.pdf'

    if os.path.isfile(background_pdf_path):
        # overlay the picture onto the background template (e.g. logo/text)
        overlay_file = f'{pictures_location}/'+filename+'_overlay.pdf'

        overlay = FPDF('P', 'mm', (100, 150))
        overlay.add_page()
        overlay.image(name=pic, x=5, y=20, w=90, h=70, link=pic)
        overlay.output(overlay_file, 'F')

        background_page = PdfReader(background_pdf_path).pages[0]
        overlay_page = PdfReader(overlay_file).pages[0]
        background_page.merge_page(overlay_page)

        writer = PdfWriter()
        writer.add_page(background_page)
        with open(out_file, 'wb') as f:
            writer.write(f)

        os.remove(overlay_file)

        print("pdf ready (with background template)")
    else:
        pdf = FPDF('P', 'mm', (100, 150))
        pdf.add_page()
        #pdf.set_font('Arial', 'B', 16)
        #pdf.cell(40, 5, 'MATTHIAS & CELINE')
        pdf.image(name=pic, x =5, y = 20, w = 90, h = 70, link = pic)

        pdf.output(out_file, 'F')

        print("pdf ready")

def print_picture(filename):

    print("printing")
    generate_pdf(filename)

    full_path = f'{pictures_location}/'+filename+'.pdf'
    print(full_path)
    print (subprocess.check_output(['lp',full_path]))

if __name__ == '__main__':

    #start_photo_seq()
    #quit()

    try:        
        setup_gpio()
        button_loop()
    finally:
        destory_gpio()

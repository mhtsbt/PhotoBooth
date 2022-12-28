import time
import RPi.GPIO as GPIO
import pygame
import pygame.camera
from fpdf import FPDF
import subprocess
from PIL import Image 

# config
button_delay = 0.1
button_pin = 12
button_led_pin = 11
smile_led_pin = 16
enable_print = False

#subprocess.run(["amixer","set","PCM","--","100%"])


# camera setup
pygame.init()

pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))

pygame.mixer.init()

def button_pressed():
    return (GPIO.input(button_pin) == 1)

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
        #print("waiting")
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

    print("cheeeeese :)")
    time.sleep(6)

    print("Taking picture")
    take_picture(filename)

    if enable_print:
        print_picture(filename)
    print("ready")
 #   turn_smile_led_off()
    return

def setup_gpio():

    GPIO.setmode(GPIO.BOARD)

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
    filename = '/home/photobooth/Pictures/'+filename+'.jpg'

    data = pygame.image.tostring(img, 'RGB')
    pil_img = Image.frombytes('RGB', img.get_size(), data)
    pil_img.save(filename)

    #pygame.image.save(img, filename)
    cam.stop()

def generate_pdf(filename):

    pic = '/home/pi/pics/'+filename+'.jpg'
    out_file = '/home/pi/pics/'+filename+'.pdf'

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

    full_path = '/home/pi/pics/'+filename+'.pdf'
    print(full_path)
    print (subprocess.check_output(['lp',full_path]))

if __name__ == '__main__':

    start_photo_seq()
    quit()

    try:        
        setup_gpio()
        button_loop()
    finally:
        destory_gpio()

import pygame
import pygame.camera

pygame.camera.init()

cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()
img = cam.get_image()
pygame.image.save(img,"filename.jpg")

from fpdf import FPDF

pdf = FPDF('P', 'mm', (100, 150))
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(40, 5, 'MATTHIAS & CELINE')
pdf.image(name="filename.jpg", x =5, y = 20, w = 90, h = 70, link = 'filename.jpg')

pdf.output('tuto1.pdf', 'F')


import subprocess
print (subprocess.check_output(['lp','tuto1.pdf']))

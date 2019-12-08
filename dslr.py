from fpdf import FPDF
import subprocess
import cv2
import time
from shutil import copyfile

IMG_TEMP_FILEN = "capt0000.jpg"
OUTPUT_PDF = "out.pdf"

def take_picture():
	process = subprocess.Popen("gphoto2 --capture-image-and-download --force-overwrite", shell=True, stdout=subprocess.PIPE)
	process.wait()
	print(process.returncode)
	print("Picture taken")

def store_picture():
	copyfile(IMG_TEMP_FILEN, f"./pictures/{time.time()}.jpg")

def resize_picture():
	img = cv2.imread(IMG_TEMP_FILEN)
	img = cv2.resize(img, None, fx=0.2, fy=0.2)
	cv2.imwrite("out.jpg", img)

def generate_pdf():

    pdf = FPDF('P', 'mm', (100, 150))
    pdf.add_page()
#    pdf.set_font('Arial', 'B', 16)
#    pdf.cell(40, 5, 'MATTHIAS & CELINE')
    pdf.image(name="out.jpg", x =5, y = 20, w = 90, h = 70, link = "out.jpg")

    pdf.output(OUTPUT_PDF, 'F')

    print("pdf ready")

def print_pdf():
	print (subprocess.check_output(['lp', OUTPUT_PDF]))


take_picture()
store_picture()
resize_picture()
generate_pdf()
print_pdf()

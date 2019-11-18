from fpdf import FPDF
import subprocess
import cv2

def take_picture():

	process = subprocess.Popen("gphoto2 --capture-image-and-download --force-overwrite", shell=True, stdout=subprocess.PIPE)
	process.wait()
	print(process.returncode)

#take_picture()

def resize_picture(fname):
	img = cv2.imread(fname)
	img = cv2.resize(img, None, fx=0.2, fy=0.2)
	cv2.imwrite("test2.jpg", img)

def generate_pdf(filename):

    pdf = FPDF('P', 'mm', (100, 150))
    pdf.add_page()
#    pdf.set_font('Arial', 'B', 16)
#    pdf.cell(40, 5, 'MATTHIAS & CELINE')
    pdf.image(name=filename, x =5, y = 20, w = 90, h = 70, link = filename)

    pdf.output("out.pdf", 'F')

    print("pdf ready")

def print_pdf():
	print (subprocess.check_output(['lp', "out.pdf"]))


resize_picture("test.jpg")
generate_pdf("test2.jpg")
print_pdf()

############ Important #############

# Check for Reason for Leave and Permanent Address

# Box ends at x-coordinate 540
# gen.addText('Hi',(540,192))
# Box ends when length of text becomes > 48
# Example : print(len('Jains Swarnakamal 69, Arcot Rd, AVM Nagar, Salig'))

from PyPDF2 import PdfWriter, PdfReader, Transformation
import io
from reportlab.pdfgen.canvas import Canvas

class GenerateFromTemplate:
    def __init__(self, template):
        self.template_pdf = PdfReader(open(template, "rb"))
        self.template_page = self.template_pdf.pages[0]

        self.packet = io.BytesIO()
        self.c = Canvas(self.packet, pagesize=(self.template_page.mediabox.width, self.template_page.mediabox.height))

    def addText(self, text, point):
        self.c.drawString(point[0], point[1], text)

    def merge(self):
        self.c.save()
        self.packet.seek(0)
        result_pdf = PdfReader(self.packet)
        result = result_pdf.pages[0]

        self.output = PdfWriter()

        op = Transformation().rotate(0).translate(tx=0, ty=0)
        result.add_transformation(op)
        self.template_page.merge_page(result)
        self.output.add_page(self.template_page)

    def generate(self, dest):
        outputStream = open(dest, "wb")
        self.output.write(outputStream)
        outputStream.close()


gen = GenerateFromTemplate("Leave_form-1.pdf")
# gen.addText('2/11/23',(480,635)) # Date
# gen.addText("A.Abineth",(300,610)) # Name
# gen.addText("211101",(300,570)) # Roll Number
# gen.addText("329",(300,540)) # Room Number
# gen.addText("CSE",(300,510)) # Department
# gen.addText("3rd year / 5th semester",(300,470)) # Year / Semester
# 
# # Adding two lines as reason for leave can be quite long and length(text) must be < 48
# 
# gen.addText('Going to Home Dussehra Holidays', (275,430)) # Reason for Leave
# gen.addText('Chennai Tamilnadu', (275,418)) # Reason for Leave
# 
# gen.addText('27/11/23',(285,370)) # Leaving Date
# gen.addText('6:00 pm',(480,370)) # Leaving Time
# gen.addText('30/11/23',(285,340)) # Return Date
# gen.addText('5:00 am',(480,340)) # Return Time
# 
# gen.addText("1234567890",(300,300)) # Student Mobile Number
# gen.addText("1234567890",(300,260)) # Father Mobile Number
# gen.addText("1234567890",(300,220)) # Mother Mobile Number
# 
# # Adding two lines as address can be quite long and length(text) must be < 48
# 
# gen.addText("Jains Swarnakamal 69, Arcot Rd, AVM Nagar",(275,192)) # Permanent Address
# gen.addText("Saligramam, Chennai, Tamil Nadu 600093",(275,180)) # Permanent Address
# 
# gen.addText('Abineth',(100,115)) # Student Signature
# gen.addText('Warden',(400,115)) # Warden Signature
# 
# gen.addText('Deputy Warden',(100,45)) # Deputy Warden Signature
# gen.addText('Chief Warden',(400,45)) # Chief Warden Signature

points = [(480,635),(300,610),(300,570),(300,540),(300,510),(300,470),(275,430),
          (275,418),(285,370),(480,370),(285,340),(480,340),(300,300),(300,260),
          (300,220),(275,192),(275,180),(100,115),(400,115),(100,45),(400,45)]

for i in range(len(points)):
    text = input('Enter a text : ')
    coordinates = points[i]
    gen.addText(text,(coordinates[0], coordinates[1]))

gen.merge()
gen.generate("Output.pdf")


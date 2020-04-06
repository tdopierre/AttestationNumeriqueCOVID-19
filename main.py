from PyPDF2 import PdfFileWriter, PdfFileReader
import qrcode
import datetime
from PIL import ImageFont
from PIL import ImageDraw
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

import argparse


# Motifs
# travail-courses-sante-famille-sport-judiciaire-missions

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-name", required=True, type=str)
    parser.add_argument("--last-name", required=True, type=str)
    parser.add_argument("--birth-date", required=True, type=str, help="DD/MM/YYYY")
    parser.add_argument("--birth-city", required=True, type=str)
    parser.add_argument("--address", required=True, type=str, help="Address Postcode City")
    parser.add_argument("--current-city", required=True, type=str)
    parser.add_argument("--leave-date", required=True, type=str, help="DD/MM/YYYY")
    parser.add_argument("--leave-hour", required=True, type=str, help="HH:MM")
    parser.add_argument("--motifs", required=True, type=str, help="- delimited: travail-courses-sante-famille-sport-judiciaire-missions")

    return parser.parse_args()


args = parse_args()
print("Args:", args)
img = Image.open("input-new.png-1.png")
img_array = np.array(img)
img_array[300:330, 250:] = 255
img_array[355:390, 250:] = 255
img_array[400:430, 185:] = 255
img_array[450:490, 270:] = 255
img_array[895:925, 155:180] = 255
img_array[635:660, 155:180] = 255

# Erase crosses
img_array[630:660, 155:185] = 255
img_array[735:765, 155:185] = 255
img_array[820:850, 155:185] = 255
img_array[895:925, 155:185] = 255
img_array[1010:1040, 155:185] = 255
img_array[1110:1140, 155:185] = 255
img_array[1185:1215, 155:185] = 255

# Erase Current city
img_array[1260:1300, 220:527] = 255

# Erase Current date
img_array[1316:1339, 190:319] = 255

# Erase Current time
img_array[1315:1339, 409:500] = 255

# Erase Current time under QR
img_array[1442:1453, 948:1078] = 255

# Erase QR
img_array[1217:1430, 800:1100] = 255

img = Image.fromarray(img_array)


# Create crosses:
def get_cross():
    image = Image.new('RGB', (30, 30), color=(255, 255, 255))
    image_draw = ImageDraw.Draw(image)
    image_font = ImageFont.truetype("Arial.ttf", 35)
    image_draw.text((3, -4), f'X', (0, 0, 0), font=image_font)
    return np.array(image)


# travail-courses-sante-famille-sport-judiciaire-missions
img_array = np.array(img)
cross = get_cross()
if "travail" in args.motifs:
    img_array[630:660, 155:185] = cross
if "courses" in args.motifs:
    img_array[735:765, 155:185] = cross
if "sante" in args.motifs:
    img_array[820:850, 155:185] = cross
if "famille" in args.motifs:
    img_array[895:925, 155:185] = cross
if "sport" in args.motifs:
    img_array[1010:1040, 155:185] = cross
if "judiciaire" in args.motifs:
    img_array[1110:1140, 155:185] = cross
if "missions" in args.motifs:
    img_array[1185:1215, 155:185] = cross

# QR CODE
qr_text = f"Cree le: {datetime.datetime.now().strftime('%d/%m/%Y a %H:%M')};" \
          f" Nom: {args.last_name};" \
          f" Prenom: {args.first_name};" \
          f" Naissance: {args.birth_date} a {args.birth_city};" \
          f" Adresse: {args.address};" \
          f" Sortie: {args.leave_date} a {args.leave_hour};" \
          f" Motifs: {args.motifs}"

# qr_text="hyduzqhdzoiqd zqoihdpodqz"
qr = qrcode.make(qr_text, border=0)
qr = qr.resize((200, 200))
qr = np.array(qr).astype(np.uint8) * 255
qr = qr.repeat(3).reshape(qr.shape[0], qr.shape[1], -1)
# img_array = np.array(img)
img_array[1228:1428, 890:1090] = np.array(qr)
img = Image.fromarray(img_array)

# Fill args
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("Arial.ttf", 22)
font_small = ImageFont.truetype("Arial.ttf", 14)
draw.text((260, 307), f'{args.first_name} {args.last_name}', (0, 0, 0), font=font)
draw.text((255, 357), f'{args.birth_date}', (0, 0, 0), font=font)
draw.text((190, 407), f"{args.birth_city}", (0, 0, 0), font=font)
draw.text((280, 458), f"{args.address}", (0, 0, 0), font=font)

draw.text((228, 1268), f"{args.current_city}", (0, 0, 0), font=font)
draw.text((190, 1319), datetime.datetime.now().strftime("%d/%m/%Y"), (0, 0, 0), font=font)
draw.text((411, 1318), datetime.datetime.now().strftime("%H:%M"), (0, 0, 0), font=font)

draw.text((948, 1443), datetime.datetime.now().strftime("%d/%m/%Y à %H:%M"), (0, 0, 0), font=font_small)

plt.imsave("output-1.pdf", np.array(img), format="pdf")

# ---------------------------
#  Second Page (Big QR code)
# ---------------------------
img = np.array(Image.open('input-new.png-2.png'))
img[:] = 255
qr = Image.fromarray(qr)
qr = qr.resize((qr.size[0] * 3, qr.size[1] * 3))
qr = np.array(qr)
img[113:113 + qr.shape[0], 113:113 + qr.shape[1]] = qr
plt.imsave("output-2.pdf", img, format="pdf")

# --------------------
# Merge PDFs
# --------------------
pdf1 = PdfFileReader('output-1.pdf')
pdf2 = PdfFileReader('output-2.pdf')
writer = PdfFileWriter()
writer.addPage(pdf1.getPage(0))
writer.addPage(pdf2.getPage(0))
writer.write(open("output.pdf", "wb"))

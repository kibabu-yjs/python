import qrcode
import cv2
import psycopg2


db = psycopg2.connect("dbname=psyco user=postgres password=root89")
cur = db.cursor()

data = {}

cur.execute("select * from employees where empl_fname='mchenazi madiricha'")
res = cur.fetchone()
id, name, _ = res
data["matricule"] = id
data["nom"] = name

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L) 
qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")


img.save("point_qr.png")


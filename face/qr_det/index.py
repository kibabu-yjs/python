import cv2
import time
import ast
from openpyxl import load_workbook
import datetime
import sys
print(datetime.date())
sys.exit()

f_name = "pointing_reg.xlsx"
wb = load_workbook(filename= f_name)

ws = wb.active
decoded_datas = [

    {'name': 'kibabu', 'old': 23, 'dte': datetime.now()}, 
    {'name': 'kabir', 'old': 27, 'dte': datetime.now()}

]
   
# qr_cap = cv2.VideoCapture(0)
# detector = cv2.QRCodeDetector()


for d in decoded_datas:
    ws.append([d['name'], d['old']])

wb.save(f_name)
# while True:

#     res, qr_fr = qr_cap.read()

     
#     retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(qr_fr)

#     if(retval):
        
#         for d in decoded_info:
            
#             if d != "":
#                 x = ast.literal_eval (d)
#                 print(f"yiyiyi:'{x}'")
#                 if x not in decoded_datas:
#                     decoded_datas.append(x)

#             print(decoded_datas)    
#             # break  
#         #     if d != "" and d != " ":
#         #         decoded_datas.append(d)
           
#         # print(decoded_datas) 
#         # break
#     else:
#         print('404')
#         text = "no qr_code detected"  
#         font = cv2.FONT_HERSHEY_SIMPLEX

#         font_scale = 0.7
#         color = (0, 0, 0) 
#         thickness = 2

#         cv2.putText(qr_fr, text, (50, 50), font, font_scale, color, thickness, cv2.LINE_AA)

#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
#     cv2.imshow("qr_detector", qr_fr)
# qr_cap.release()
# cv2.destroyAllWindows()
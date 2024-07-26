import sys, ast, os, cv2, psycopg2, face_recognition, time
from datetime import datetime
from openpyxl import load_workbook
import configparser
import smtplib
from email.message import EmailMessage

#Variables
wb = load_workbook("pointing_reg.xlsx")
ws = wb.active
path = "."
ls = [] # the list that holds local images

face_classifier = cv2.CascadeClassifier( cv2.data.haarcascades + "haarcascade_frontalface_default.xml" )
video_capture = cv2.VideoCapture(0)

qr_cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

# Variables end

#fn
def pic_grep():

    for f in os.listdir(path= path):
        
        if os.path.splitext(f)[1][1:] in ['png', 'jpg', 'jpeg', 'gif'] :
            ls.append(f"{os.getcwd()}/{f}")

pic_grep()

def get_email_credentials():
    
  config = configparser.ConfigParser()
  config.read('email_cred.ini')
  username = config['email']['username']
  password = config['email']['password']
  return username, password


username, password = get_email_credentials()

def send_email(sender, recipient, fault_n, fault_m,  empl_n, empl_matr):
  
  email = EmailMessage()
  email['From'] = sender

  email['To'] = recipient
  email['Subject'] = "Erreur de pointage"
  email.set_content(f"🚨🚨L'employé {fault_n} matricule {fault_m}, a effectué le pointage à la place de {empl_n}, matricule {empl_matr} .")
  
  with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login("amuhammadben@gmail.com", "uget ucwv kxib dozz")
    server.send_message(email)
    server.close()

sender = username
recipient = username

def face_finder(vid):

    face_classifier.detectMultiScale(vid, 1.1, 7, minSize=(40, 50))
    return len(face_classifier.detectMultiScale(vid, 1.1, 7, minSize=(40, 50)))
    return [faces, insert]

def pointer(vid, m, fn):
    
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    face_components = face_recognition.face_landmarks(gray_image)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 7, minSize=(40, 50))
    detector = cv2.QRCodeDetector()

    # for return handling
    esc_point = False
    insert = False

    if len(faces) > 0 :

        if len(face_components) > 0:
            
            #landmarks
            right_eye = 'right_eye' in face_components[0]
            left_eye = 'left_eye' in face_components[0]

            top_lip = 'top_lip' in face_components[0]
            bottom_lip = 'bottom_lip' in face_components[0]
            chin = 'chin' in face_components[0]
            
            #landmarks
            if right_eye and left_eye and top_lip and bottom_lip and chin:
                
                cv2.imwrite(f"{os.getcwd()}/face/scanned_pics/1.jpg", gray_image)
                img = face_recognition.load_image_file(f"{os.getcwd()}/face/scanned_pics/1.jpg")
                
                img_path = os.getcwd() + "/face/scanned_pics/1.jpg"
                
                pic_enc = face_recognition.face_encodings(img)[0]
                
                #scanning through uploaded images
                for i in ls:
                    
                    pic_i = face_recognition.load_image_file(f'{i}')
                    pic_i_enc = face_recognition.face_encodings(pic_i)
                    compare = face_recognition.compare_faces( pic_i_enc, pic_enc, tolerance=0.6 )
                    
                    if len(compare) > 0:
                        
                        # Scanning Unix like fs
                        if compare[0] == True and '/' in i:
                           
                            fetch_str = i[ i.rfind('/') + 1 : i.rfind('.') ]

                            db = psycopg2.connect(" dbname= psyco user= postgres password= root89 ")
                            cur = db.cursor()

                            cur.execute(f"select * from employees where empl_img_name = '{fetch_str}' ")
                            rec = cur.fetchone()
                            
                            e_id, fname, e_img = rec
                            pointing_date = datetime.now()

                            if e_id == m:
                                
                                try:
                                    cur.execute( "insert into pointing_records(empl_id, empl_time, empl_fname) values (%s, %s, %s)", (e_id, pointing_date, fname) )
                                    # a boring tuple with datas for excel_file
                                    to_save = (pointing_date, m, fn)
                                    
                                    ws.append(to_save)
                                    wb.save("pointing_reg.xlsx")
                                    db.commit()
                                    
                                    cur.close()
                                    db.close()
                                    print("pointing succeeded 🤗✅")
                                    insert= True

                                except Exception as err:                          
                                    print(f'inserting stack trace: {err}')


                            else:
                                try:
                                    cur.execute( "insert into pointing_records(empl_id, empl_time, empl_fname) values (%s, %s, %s)", (e_id, pointing_date, fname) )
                                    # a boring tuple with datas for excel_file
                                    to_save = (pointing_date, m, fn)
                                    
                                    ws.append(to_save)
                                    wb.save("pointing_reg.xlsx")
                                    # db.commit()
                                    
                                    cur.close()
                                    db.close()
                                    insert= True

                                    # sending email to the admin 
                                    send_email(sender,sender, fname, e_id, fn, m)
                                    print("pointing succeeded 🤗✅")

                                except Exception as err:                          
                                    print(f'inserting stack trace: {err}')
                            

                        # Scanning windows like fs
                        elif compare[0] == True and '\\' in i:

                            fetch_str = i[ i.rfind('\\') + 1 : i.rfind('.') ]
                            cur.execute(f"select * from employees where empl_img_name = '{fetch_str}' ")

                            rec = cur.fetchone()
                            e_id, fname, e_img = rec

                            pointing_date = datetime.now()

                            if e_id == m:
                                
                                try:
                                    cur.execute("insert into pointing_records(empl_id, empl_time, empl_fname) values (%s, %s, %s)", (e_id, pointing_date, fname) )
                                    # a boring tuple with datas for excel_file
                                    to_save = (pointing_date, m, fn)
                                    
                                    ws.append(to_save)
                                    wb.save("pointing_reg.xlsx")
                                    # db.commit()
                                    
                                    cur.close()
                                    db.close()
                                    print("pointing succeeded 🤗✅")
                                    insert= True

                                except Exception as err:                          
                                    print(f'inserting stack trace: {err}')


                            else:
                                
                                try:
                                
                                    cur.execute( "insert into pointing_records(empl_id, empl_time, empl_fname) values (%s, %s, %s)", (e_id, pointing_date, fname) )
                                    # a boring tuple with datas for excel_file
                                    to_save = (pointing_date, m, fn)
                                    
                                    ws.append(to_save)
                                    wb.save("pointing_reg.xlsx")
                                    # db.commit()
                                    
                                    cur.close()
                                    db.close()

                                    insert= True
                                    # sending email to the admin 
                                    send_email(sender, sender, fname, e_id, fn, m)
                                    print("pointing succeeded 🤗✅")
                                
                                except Exception as err:                          
                                    print(f'inserting stack trace: {err}')


                            
                        elif compare[0] == False:
                            
                            pointing_date = datetime.now()
                            to_save = (pointing_date, m, fn)
                            
                            ws.append(to_save)
                            wb.save("pointing_reg.xlsx")
                            
                            email = EmailMessage()
                            email['From'] = sender

                            email['To'] = recipient
                            email['Subject'] = "Erreur de pointage"

                            email.set_content(f"🚨🚨Un inconnu a effectué le pointage à la place de {fn}, matricule {m}.")
                            server = smtplib.SMTP('smtp.gmail.com', 587)

                            server.starttls()
                            server.login("amuhammadben@gmail.com", "uget ucwv kxib dozz")
                            server.send_message(email)
                            server.close()
                            
                            insert = True                                                                 
                            
    return [faces, insert, esc_point]

def success_text(vid):

    text = "ok"  
    font = cv2.FONT_HERSHEY_SIMPLEX

    font_scale = 0.7
    color = (0, 0, 0) 

    thickness = 2
    cv2.putText(vid, text, (40, 42), font, font_scale, color, thickness)
    
#fn end    

k = False
l = False

while True:

    result, video_frame = video_capture.read() 
    
    getter = face_finder(video_frame)
    key = cv2.waitKey(1) & 0xFF

    if getter < 1:
        
        text = "jig saw"  
        font = cv2.FONT_HERSHEY_SIMPLEX

        font_scale = 0.7
        color = (0, 255, 0) 
        thickness = 2

        cv2.putText(video_frame, text, (20, 20), font, font_scale, color, thickness, cv2.LINE_AA)    

    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(video_frame)
    
    if len(decoded_info) < 1:
        
        text = "QRcode non apparent"  
        font = cv2.FONT_HERSHEY_SIMPLEX

        font_scale = 0.7
        color = (0, 255, 0)

        thickness = 2
        cv2.putText(video_frame, text, (20, 50), font, font_scale, color, thickness, cv2.LINE_AA)    


    if key == ord("s") and len(decoded_info) >= 1 and getter >=1 :
        
        print("🎥🎥🎥....pointing")

        try:
            
            dt = decoded_info[0]
            real_dict = ast.literal_eval(dt)

            faces = pointer(video_frame, real_dict['matricule'], real_dict['nom'])
            k = True if faces[1] == True else False
            l = True if faces[2] == True else False

        except Exception as err:
            print(f"An error {err}")
    
    if key == ord("q"):
        faces = []
    
    if k:
        
        faces = success_text(video_frame)

    if l:

        try:
            pass
            # dt = decoded_info[0]
            # real_dict = ast.literal_eval(dt)
            # send_email(sender, sender, real_dict['matricule'], real_dict['nom'])
            # faces = success_text(video_frame) 
            # key = ord("q")
        except Exception as err:
            print(err)

    if key == ord("e"):

        print("Releasing camera and closing program.. 🕕")
        break
    
    if result is False:
        break  
    
    cv2.imshow("Pointer", video_frame) 

video_capture.release()
cv2.destroyAllWindows()

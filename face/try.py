import cv2, face_recognition

stream = cv2.VideoCapture(0)
face_classifier = cv2.CascadeClassifier( cv2.data.haarcascades + "haarcascade_frontalface_default.xml" )
thing = False



def pointer(vid):

    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    face_components = face_recognition.face_landmarks(gray_image)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 7, minSize=(40, 50))

    if len(faces) > 0:
        print ('face found')
    else:
        print('face not found')    
    while True:

        res, real_str = stream.read()
        key = cv2.waitKey(1) & 0xFF
        faces = []

        if key == ord("s"):
            pointer(real_str)

        if key == ord("q"):
            break    
        
        cv2.imshow("timer", real_str)

    stream.release()
    cv2.destroyAllWindows()        






# while True:

#     res, real_str = stream.read()

#     key = cv2.waitKey(1) & 0xFF
#     faces = []

#     if key == ord("s"):
#         pointer(real_str)

#     if key == ord("q"):
#         break    
#     cv2.imshow("timer", real_str)

# stream.release()
# cv2.destroyAllWindows()
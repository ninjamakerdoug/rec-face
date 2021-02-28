# -*- coding: cp1252 -*-

import face_recognition
import cv2
import numpy as np
import os
from sklearn import svm
import time
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
#video_capture = cv2.VideoCapture(0)

encodings = []
names = []

# Training directory
train_dir = os.listdir('BancoDeDados')

# Loop through each person in the training directory
for person in train_dir:
    pix = os.listdir("BancoDeDados/" + person)

    # Loop through each training image for the current person
    for person_img in pix:
        # Get the face encodings for the face in each image file
        face = face_recognition.load_image_file("BancoDeDados/" + person + "/" + person_img)
        face_bounding_boxes = face_recognition.face_locations(face)

        #If training image contains exactly one face
        if len(face_bounding_boxes) == 1:
            face_enc = face_recognition.face_encodings(face)[0]
            # Add face encoding for current image with corresponding label (name) to the training data
            encodings.append(face_enc)
            names.append(person)
        else:
            print(person + "/" + person_img + " <<imagem rejeitada>>")
            os.remove("BancoDeDados/" + person + "/" + person_img)


# Create and train the SVC classifier
clf = svm.SVC(gamma='scale')
clf.fit(encodings,names)


def analisar():
    video_capture = cv2.VideoCapture(0)
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(encodings, face_encoding)
                name = "Desconhecido"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = names[best_match_index]

                face_names.append(name)
            

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            for x in face_names:
                return x
            break

    # Release handle to the webcam
    video_capture.release()



def mostrarCam():
    video_capture = cv2.VideoCapture(0)
    fourcc=cv2.VideoWriter_fourcc(*'XVID') 
    op=cv2.VideoWriter('video.mp4',fourcc,11.0,(640,480))
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(encodings, face_encoding)
                name = "Desconhecido"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = names[best_match_index]

                face_names.append(name)
            

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        op.write(frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #print('\nFaces reconhecidas:'+('\n'))
            for x in face_names:
                print('\n')
            break

    # Release handle to the webcam
    op.release()
    video_capture.release()
    cv2.destroyAllWindows()


def carregaNomesASeremLidos(txt):
    listaNomeYoutubers = []
    pFile = open(txt, "r")
    for line in pFile:
        listaNomeYoutubers.append(line.rstrip())
    return listaNomeYoutubers

def criaPastaComNomes(listaNomes):
    for nome in listaNomes:
        if nome == 'teste':
            os.mkdir('./teste/')
        else:
            try:
                os.mkdir('./BancoDeDados/'+nome)
            except OSError:
                print("Não foi possível criar o diretório ou o mesmo já existe.")

                

def salvaFacesDetectadas(nome):
    face_cascade = cv2.CascadeClassifier('./Haarcascade/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0) #inicia captura da câmera
    counterFrames = 0
    while(counterFrames < 10): #quando chegar ao quinto frame, para
        #print(counterFrames)
        ret, img = cap.read()

        #frame não pode ser obtido? entao sair
        if(ret == False):
            cap.release()
            return

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        #se nenhuma face for achada, continue
        if not np.any(faces):
            continue

        #achou uma face? recorte ela (crop)
        for (x, y, w, h) in faces:
            rostoImg = img[y:y+h, x:x+w]

        #imagens muito pequenas são desconsideradas
        larg, alt, _ = rostoImg.shape
        if(larg * alt <= 20 * 20):
            continue

        #salva imagem na pasta
        rostoImg = cv2.resize(rostoImg, (255, 255))
        if nome == 'teste':
            cv2.imwrite("./"+ nome + "/" + str(counterFrames)+".jpg", rostoImg)
        else:
            cv2.imwrite("./BancoDeDados/" + nome + "/" + str(counterFrames)+".jpg", rostoImg)
        counterFrames += 1
            
    cap.release()


def carregarImg(txt):
    pix = os.listdir("BancoDeDados/" + txt)
    contar = 0

    # Loop through each training image for the current person
    for person_img in pix:
        # Get the face encodings for the face in each image file
        face = face_recognition.load_image_file("BancoDeDados/" + txt + "/" + person_img)
        face_bounding_boxes = face_recognition.face_locations(face)

        #If training image contains exactly one face
        if len(face_bounding_boxes) == 1:
            face_enc = face_recognition.face_encodings(face)[0]
            # Add face encoding for current image with corresponding label (name) to the training data
            encodings.append(face_enc)
            names.append(txt)
        else:
            #print(txt + "/" + person_img + " <<imagem rejeitada>>")
            os.remove("BancoDeDados/" + txt + "/" + person_img)
            contar += 1

    if contar == 5:
        #apagar pasta criada caso nenhuma foto seja salva
        os.rmdir("BancoDeDados/" + txt)
        contar = 0
        #print('\nAs imagens não estão claras para o reconhecimento, tente novamente...')
        return 'Desculpe, não entendi, pode repetir por favor?'
    elif contar > 0 and contar < 5:
        return 'ok'
        #print('\nFace salva no Banco de Dados.')


def gravarVideo():
   capture =cv2.VideoCapture(0)
   face_cascade = cv2.CascadeClassifier('./Haarcascade/lbpcascade_frontalface.xml')
   eye_glass = cv2.CascadeClassifier('./Haarcascade/haarcascade_eye_tree_eyeglasses.xml')
   fourcc=cv2.VideoWriter_fourcc(*'XVID') 
   op=cv2.VideoWriter('video.avi',fourcc,9.0,(640,480))

   while True:
       ret, frame = capture.read()
       gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       faces = face_cascade.detectMultiScale(gray)
    

       for (x,y,w,h) in faces:
           font = cv2.FONT_HERSHEY_COMPLEX
           cv2.putText(frame,'Face',(x+w,y+h),font,1,(250,250,250),2,cv2.LINE_AA)
           cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
           roi_gray = gray[y:y+h, x:x+w]
           roi_color = frame[y:y+h, x:x+w]
        
          

           eye_g = eye_glass.detectMultiScale(roi_gray)
           for (ex,ey,ew,eh) in eye_g:
              cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
       op.write(frame)
       #cv2.imshow('frame',frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
          break
   op.release()      
   capture.release()
   #cv2.destroyAllWindows()


#função principal da aplicação de salvamento de faces
def main():
    listaNomeYoutubers = carregaNomesASeremLidos("input.txt")
    criaPastaComNomes(listaNomeYoutubers)

    for nome in listaNomeYoutubers:
        salvaFacesDetectadas(nome)
    time.sleep(3)
    carregarImg(nome)
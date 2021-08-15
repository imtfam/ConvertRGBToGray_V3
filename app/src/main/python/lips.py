import numpy as np
import cv2
from  PIL import Image
import base64
import io
import face_recognition
from  PIL import  ImageColor


def creatorBox(img, points, scale = 2, masked = False, cropped = True):
    if masked:
        mask = np.zeros_like(img)
        mask = cv2.fillPoly(mask, [points], (255, 255, 255))
        #cv2.imshow('Mask', mask)
        img = cv2.bitwise_and(img, mask)
    if cropped:
        bbox = cv2.boundingRect(points)
        x, y, w, h = bbox
        imgCrop = img[y:y+h, x:x+w]
        imgCrop = cv2.resize(imgCrop, (0, 0), None ,scale, scale)
        return imgCrop
    else:
        return mask

def main(data,color):
    decoded_data = base64.b64decode(data)
    np_data = np.fromstring(decoded_data,np.uint8)
    img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #####

    #image = face_recognition.load_image_file("image/1.jpg")
    face_landmarks_list = face_recognition.face_landmarks(img)

    lips = []
    pointLandmarks = []

    for face_landmarks in face_landmarks_list:
        for i in range(len(face_landmarks['top_lip'])):
            lips.append((face_landmarks['top_lip'][i]))
        for i in range(len(face_landmarks['bottom_lip'])):
            lips.append((face_landmarks['bottom_lip'][i]))



    #img = cv2.imread('image/1.jpg')
    #success, img = cap.read()
    img = cv2.resize(img, (0, 0), None, 1, 1)
    imgOriginal = img.copy()

    for i in range(len(lips)):
        x = lips[i][0]
        y = lips[i][1]
        pointLandmarks.append((x, y))

    pointLandmarks = np.array(pointLandmarks)
    print(pointLandmarks)

    imgLips = creatorBox(img, pointLandmarks, masked = True, cropped = False)

    imgColorLips = np.zeros_like(imgLips)
    imgColorLips[:] = 255,0,0
    imgColorLips = cv2.bitwise_and(imgLips, imgColorLips)
    imgColorLips = cv2.GaussianBlur(imgColorLips, (7, 7), 10)
    imgColorLips = cv2.addWeighted(imgOriginal, 1, imgColorLips, 1, 0)
    print(type(imgColorLips));

    pil_im = Image.fromarray(imgColorLips)


    #####
    #convert image to Byte
    buff=io.BytesIO()
    pil_im.save(buff,format = "PNG")
    #conver it again to base64
    img_str = base64.b64encode(buff.getvalue())
    return ""+str(img_str,'utf-8')
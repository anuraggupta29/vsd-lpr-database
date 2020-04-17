import cv2
import  imutils
import pytesseract
from datetime import datetime
from time import sleep
from twilio.rest import Client
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dlib import correlation_tracker, rectangle as dlib_rectangle
from numpy import array as nparray
from threading import Thread

def blackout(img):
    xBlack = 360
    yBlack = 300
    triangle_cnt = nparray( [[0,0], [xBlack,0], [0,yBlack]] )
    triangle_cnt2 = nparray( [[WIDTH,0], [WIDTH-xBlack,0], [WIDTH,yBlack]] )
    cv2.drawContours(img, [triangle_cnt], 0, (0,0,0), -1)
    cv2.drawContours(img, [triangle_cnt2], 0, (0,0,0), -1)

    return img

def estimateSpeed(carID):
    timeDiff = (endTracker[carID]-startTracker[carID]).total_seconds()
    spd = round(markGap/timeDiff*3.6,2)

    return spd

def licenseProgram():
    while True:
        if len(overSpeedArr)>0:
            timestamp1, spd1, img1 = overSpeedArr.pop(0)
            licPlateImage = None
            licNo1  = None
            imgFile = img1

            licNo1,licPlateImage = getLicenseNo(imgFile)
            #viewResults(image, licPlateImage, licNo)

            licenseDataArr.append((timestamp1, spd1, licNo1, img1))
            print('Thread 1 Complete')
        else:
            sleep(2.0)

def getLicenseNo(imgFile):
    licNoF = None
    licPlateImgF = None

    #RESIZE THE IMAGE
    heightF, widthF = imgFile.shape[0:2]
    imgFile = imgFile[heightF//2:heightF, 0:widthF]

    resizeWidth = 960

    if (imgFile.shape[1]>resizeWidth):
        imgFile = imutils.resize(imgFile, width=resizeWidth)

    areaTH = (imgFile.shape[0]*imgFile.shape[1])//1000

    #APPLY FILTERS ON IMAGE
    imgF = cv2.cvtColor(imgFile, cv2.COLOR_BGR2GRAY)
    imgF = cv2.bilateralFilter(imgF, 11, 17, 17)
    imgF = cv2.Canny(imgF, 170, 200)

    #FIND ALL CONTOURS
    cnts = cv2.findContours(imgF, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]

    for i in cnts:
        if cv2.contourArea(i) > areaTH:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if (len(approx) == 4):

                x,y,w,h = cv2.boundingRect(approx)
                licPlateImgF = imutils.resize(imgFile[y:y+h, x:x+w], width=200)

                #RUN TESSERACT OCR ON IMAGE------
                textTemp = pytesseract.image_to_string(licPlateImgF, config=config)

                if (len(textTemp)>=4):
                    licNoF = ""
                    for i in textTemp:
                        if (i.isalnum() == True):
                            licNoF += i.upper()
                    break

    return licNoF,licPlateImgF

def viewResults(img1,licPlateImage,licNo1):
    cv2.imshow("Car Image", imutils.resize(img1, width=540))
    try:
        cv2.imshow("License Plate",licPlateImage)
    except:
        pass
    print("License Number : ", licNo)
    cv2.waitKey(0)

def storeData():
    while True:
        if len(licenseDataArr)>0:
            timestamp2, spd2, licNo2, img2 = licenseDataArr.pop(0)
            date2 = timestamp2.strftime("%Y-%m-%d")
            time2 = timestamp2.strftime("%H: %M: %S")

            if licNo2 == None:
                licNo2 = 'NULL'
                licError = 1

            dataDict = {'date': date2, 'time': time2, 'speed': spd2, 'licNo': licNo2, 'licError': licError}
            db.collection(u'overspeed').add(dataDict)

            print('thread2 complete')
        else:
            sleep(2.0)

def sendSMS():
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body="Your text here",
                         from_='',#your twilio phone number
                         to='+91'+str("ENTER RECIEVER CONTACT NUMBER")
                     )

    return message.sid


#CONNECT TO FIREBASE PROJECT----------------------------------------------------
#this credential you can obtain from project settings in firebase
cred = credentials.Certificate('vsd-lpr-json-key.json')

try:
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print ("Connected to Cloud FireStore")

except:
    print ("Unable to Connect")

#DATA FOR THREADS---------------------------------------------------------------
overSpeedArr = []
licenseDataArr = []

#CREATING THREADS---------------------------------------------------------------
t1 = Thread(target=licenseProgram)
t2 = Thread(target=storeData)

t1.start()
t2.start()

#CLASSIFIER FOR DETECTING CARS--------------------------------------------------
carCascade = cv2.CascadeClassifier('files/HaarCascadeClassifier.xml')

#LIBRARY FOR TEXT RECOGNITION---------------------------------------------------
config = ('-l eng --oem 1 --psm 3') #TESSERACT CONFIGURATION

#TAKE VIDEO---------------------------------------------------------------------
video = cv2.VideoCapture('files/videoTest.mp4')
starttime = datetime.now().replace(microsecond=0)
print('Start Time : ', starttime)

#VARIABLES----------------------------------------------------------------------
WIDTH = 1280 #width of video frame
HEIGHT = 720 #height of video frame
cropBegin = 240 #crop video frame from this point
mark1 = 120 #mark to start timer
mark2 = 360 #mark to end timer
markGap = 15 #distance in metres between the markers
fpsFactor = 3 #to compensate for slow processing
speedLimit = 20 #speedlimit
startTracker = {} #store starting time of cars
endTracker = {} #store ending time of cars
carTracker = {} #store car details
rectangleColor = (0, 255, 0)
frameCounter = 0 #Number of current frame
currentCarID = 0 #current car ID

print('Speed Limit Set at 20 Kmph')

#TRACK CARS---------------------------------------------------------------------
while True:
    rc, image = video.read()
    if type(image) == type(None):
        break

    frameTime = datetime.now()
    image = cv2.resize(image, (WIDTH, HEIGHT))[cropBegin:720,0:1280]
    resultImage = blackout(image)
    #cv2.line(resultImage,(0,mark1),(1280,mark1),(0,0,255),2)
    #cv2.line(resultImage,(0,mark2),(1280,mark2),(0,0,255),2)

    frameCounter = frameCounter + 1
    if (frameCounter == 1000):
        break

    #DELETE CARIDs NOT IN FRAME-------------------------------------------------
    carIDtoDelete = []

    for carID in carTracker.keys():
        trackingQuality = carTracker[carID].update(image)

        if trackingQuality < 7:
            carIDtoDelete.append(carID)

    for carID in carIDtoDelete:
        carTracker.pop(carID, None)

    #MAIN PROGRAM---------------------------------------------------------------
    if (frameCounter % 60 == 0):
        gray = cv2.cvtColor(resultImage, cv2.COLOR_BGR2GRAY)
        cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24)) #DETECT CARS IN FRAME

        for (_x, _y, _w, _h) in cars:
            #GET POSITION OF A CAR
            x = int(_x)
            y = int(_y)
            w = int(_w)
            h = int(_h)

            xbar = x + 0.5*w
            ybar = y + 0.5*h

            matchCarID = None

            #IF CENTROID OF CURRENT CAR NEAR THE CENTROID OF ANOTHER CAR IN PREVIOUS FRAME THEN THEY ARE THE SAME
            for carID in carTracker.keys():
                trackedPosition = carTracker[carID].get_position()

                tx = int(trackedPosition.left())
                ty = int(trackedPosition.top())
                tw = int(trackedPosition.width())
                th = int(trackedPosition.height())

                txbar = tx + 0.5 * tw
                tybar = ty + 0.5 * th

                if ((tx <= xbar <= (tx + tw)) and (ty <= ybar <= (ty + th)) and (x <= txbar <= (x + w)) and (y <= tybar <= (y + h))):
                    matchCarID = carID


            if matchCarID is None:
                tracker = correlation_tracker()
                tracker.start_track(image, dlib_rectangle(x, y, x + w, y + h))

                carTracker[currentCarID] = tracker

                currentCarID = currentCarID + 1


    for carID in carTracker.keys():
        trackedPosition = carTracker[carID].get_position()

        tx = int(trackedPosition.left())
        ty = int(trackedPosition.top())
        tw = int(trackedPosition.width())
        th = int(trackedPosition.height())

        #PUT BOUNDING BOXES-----------------------------------------------------
        #cv2.rectangle(resultImage, (tx, ty), (tx + tw, ty + th), rectangleColor, 2)
        #cv2.putText(resultImage, str(carID), (tx,ty-5), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 1)

        #ESTIMATE SPEED---------------------------------------------------------
        if carID not in startTracker and mark2 > ty+th > mark1 and ty < mark1:
            startTracker[carID] = frameTime

        elif carID in startTracker and carID not in endTracker and mark2 < ty+th:
            endTracker[carID] = frameTime
            speed = estimateSpeed(carID)
            if speed > speedLimit:
                print('CAR-ID : {} : {} kmph - OVERSPEED'.format(carID, speed))

                overSpeedArr.append((frameTime, speed, image[ty:ty+th, tx:tx+tw]))

            else:
                print('CAR-ID : {} : {} kmph'.format(carID, speed))

            del startTracker[carID]
            del endTracker[carID]

    #DISPLAY EACH FRAME
    #cv2.imshow('result', resultImage)

    #if cv2.waitKey(33) == 27:
    #    break

video.release()
endtime = datetime.now().replace(microsecond=0)
print('End Time : ', endtime)
print('Total time taken is : ', endtime-starttime)
#cv2.destroyAllWindows()

Created by Anurag Gupta
-Project still under development

1. uses haarcascade classifier to detect cars
2. uses tesseract to detect text
3. uses openCV for image manipulations and enhancements
4. uses firebase cloud firestore as a database (main_firebase.py) - online
5. uses firebase cloud storage to store car images (main_firebase_image.py) - online
6. uses ibm db2 cloud database (main_ibm_db2.py) - optional
5. uses sqlite database (main_sqlite.py) - local
8. can just view and save overspeeding car image (main_saveimage.py) - optional
6. uses twilio to send SMS
7. uses multithreading to execute speed detection, license detection and storing data in parallel
8. a single webpage to view the data in firestore collection/table along with the car image.

-database/collection:
-contains following fields/columns - {'date', 'time', 'speed', 'licNo', 'licError'}
-main_firebase_image.py contains an additional 'imageLink' field.

for firestore:
1. create a firestore project and database service
2. A colletion 'overspeed' will be created automatically while running .py file
3. get your api-keys/credentials in json format for your python project and replace with .json file.
4. Create a firebase cloud storage instance as well (for images) and make the bucket public (google it!)

1. SENS SMS PART REQUIRES A SEPARATE TABLE WITH OWNER DETAILS and CORRESPONDING LICENSE NUMBER
2. OWENER DETAILS PART NOT IMPLEMENTED YET - FUNCTION IS PROVIDED

1. webpage has no backend can be hosted easily on github etc.
2. webpage also requires firestore credentials, can be obtained from project settings.
3. Don't host if database in test mode. it will give anyone access to database!!

1. license plate detection is often inaccurate
2. the license image obtained is low contrast, and low res around 20 by 50 px, if using 1280 by 720 video.
3. thus text recognition is so far impossible.

-for separate vehicle detection and license recognition(high res image) see other repositories.

<h4>Created by Anurag Gupta</h4>
<h5>Project still under development<h5>
  
<h2>Vehicle Speed Detection & License Plate Recognition using Computer Vision</h2>

1. Uses haarcascade classifier to detect cars.
2. Uses tesseract to detect text.
3. Uses openCV for image manipulations and enhancements.
4. Uses firebase cloud firestore as a database (main_firebase.py) - online.
5. Uses firebase cloud storage to store car images (main_firebase_image.py) - online.
6. Uses ibm db2 cloud database (main_ibm_db2.py) - optional.
5. Uses sqlite database (main_sqlite.py) - local.
8. Can just view and save overspeeding car image (main_saveimage.py) - optional.
6. Uses twilio to send SMS.
7. Uses multithreading to execute speed detection, license detection and storing data in parallel.
8. A single webpage to view the data in firestore collection/table along with the car image.

<h4>Database/Collection</h4>
<ul>
  <li>contains following fields/columns - {'date', 'time', 'speed', 'licNo', 'licError'}</li>
  <li>main_firebase_image.py contains an additional 'imageLink' field.</li>
</ul>

<h3>For Firestore</h3>

*Knowledge of firebase Required.
1. Create a firestore project and database service.
2. C colletion 'overspeed' will be created automatically while running .py file. (Can change it)
3. Get your api-keys/credentials in json format for your project and replace with .json file. (from firebase project settings)
4. Create a firebase cloud storage instance as well (for images) and make the bucket public. (google it!)

<h3>For Sqlite3</h3>

1. Stores the same details as firebase except images in the local sqlite database. (files/vsdlpr.sqlite)

<h3>for IBM Db2</h3>

1. Stores the same details as firebase except images in the ibm Db2 Cloud database.

<h3>View Video and Overspeed Details</h3>

1. Use main_saveimage.py to view the video and detection, along with estimated speed.

<h3>Sending SMS</h3>

1. Send SMS part requires a separate table with owner details and corresponding license number.
2. Owner Details part isn't implemented yet, function is provided.

<h3>Webpage to view Firebase Database</h3>

1. Webpage has no backend can be hosted easily on github etc.
2. Webpage also requires firestore credentials, can be obtained from project settings.
3. Don't host if database in test mode. it will give anyone access to database!!

<h3>Relevant Details</h3>

1. License plate detection is often inaccurate.
2. The license image obtained is low contrast, and low res around 20 by 50 px, if using 1280 by 720 video.
3. Thus text recognition is so far impossible.
4. Check my other repositories for code for License plate Recognition.

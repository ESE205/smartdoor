import boto3
import json
import picamera
import time
import requests
import RPi.GPIO as GPIO


s3 = session.client('s3')
updatedtime=time.time()
timestamp=str(round(updatedtime*1000))
client=session.client('rekognition', 'us-east-1')
bucket= 'smartdoorpictures'
FACE_LIST= ["andrew", "johnny", "katie"]
key_target= "intruder" +timestamp +".jpg"
threshold=0
RECOGNIZED_FACE = False
IS_FACE=False
region_name= 'us-east-1'
message = []
MIN_SIM= 60.0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

while True:
    input_state=GPIO.input(18)
    if input_state == False:
        #when camera is plugged in use this code
        print ("button was pushed")
        GPIO.output(17, True)
        with picamera.PiCamera() as camera:
            camera.resolution= (1280, 720)
            camera.capture('intruderface.jpg')
        GPIO.output(17, False)    
        s3.upload_file('intruderface.jpg', Bucket=bucket, Key= key_target, ExtraArgs={'ContentType':"image/jpg"})
        
        
        
        def detect_face(bucket, key, region_name = "us-east-1", attributes = ['ALL']):
            rekognition = session.client("rekognition", region_name)
            response = rekognition.detect_faces(
                Image={
                    "S3Object": {
                        "Bucket": bucket,
                        "Name": key
                        }
                    },
                    Attributes = attributes,
        )
            return response['FaceDetails']

        def compare_faces(bucket, key, bucket_target, key_target, threshold, region_name):
            rekognition = session.client("rekognition", region_name)
            response = rekognition.compare_faces(
            SourceImage={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
                }
                },
                TargetImage={
                "S3Object": {
                "Bucket": bucket_target,
                "Name": key_target,
                }
                },
                SimilarityThreshold=threshold,
                )
            return response['SourceImageFace'], response['FaceMatches']
            
        
        for face in detect_face(bucket, key_target):
            conf = face['Confidence']
            if(conf >= MIN_SIM):
                message.append("face detected")
                IS_FACE = True
            else:
                IS_FACE = False
                message.append("no face detected")
                #rerun program
        if (IS_FACE==True)  :
            for face in FACE_LIST:
                FILENAME= face + ".jpg"
                source_face, matches = compare_faces(bucket, FILENAME, bucket, key_target, threshold, region_name)
                for match in matches:
                    sim = match['Similarity']
                    message.append("simScore: " + str(sim))
                    if (sim>= MIN_SIM) :
                        message.append("user name: " + str(face))
                        RECOGNIZED_FACE = True
                        GPIO.output(22,True)
                        #turn on green light
                    
        if (RECOGNIZED_FACE ==False):
            GPIO.output(27,True)
            message.append("unknown user")
            #turn on red light
            #send text message to user


        print(str.join(',', message))
        print (key_target)
        r=requests.get("http://3.208.217.100:1337/textuser/{}".format(key_target))
        
        while True:
            if time.time()-updatedtime > 10:
                r=requests.get("http://3.208.217.100:1337/accessstatus/{}".format(key_target))
                response=json.loads(r.text)
                #if response["status"]== "approved":
                #nothing should happen or turn on green light
                # if response["status"]=="declined":
                #turn on red light
                #if response["status"]=="pending":
                #yellow light??
                print (response["status"])
                updatedtime=time.time()
                
                

            

import boto3
import json
import picamera
import datetime
import time
import requests 

#copy access key here#
s3 = session.client('s3')
timestamp=str(round(time.time()*1000))
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

if __name__ == "__main__":
    #when camera is plugged in use this code
    with picamera.PiCamera() as camera:
        camera.resolution= (1280, 720)
        camera.capture('intruderface.jpg')
    s3.upload_file('intruderface.jpg', Bucket=bucket, Key= key_target)
       
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
    if (RECOGNIZED_FACE ==False):
        message.append("unknown user")
        #turn on red light
        #send text message to user


    print(str.join(',', message))

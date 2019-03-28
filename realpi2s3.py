import boto3
import picamera
import sys
import time

session = boto3.Session(aws_access_key_id= "AKIAI2KN6Z5PTTM2O2JQ", aws_secret_access_key="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",region_name='us-east-1')
s3 = session.client('s3')
client= session.client('rekognition', 'us-east-1')

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.capture('intruderface.jpg')


BUCKET= "smartdoorpictures"
KEY_TARGET = "intruderface.jpg"


s3.upload_file('intruderface.jpg', Bucket=BUCKET, Key= KEY_TARGET)

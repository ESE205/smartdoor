import boto3
import json
#import picamera as picam
import datetime


session = boto3.Session(aws_access_key_id= "AKIAI2KN6Z5PTTM2O2JQ", aws_secret_access_key= "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", region_name='us-east-1')

s3 = session.resource('s3')
client=session.client('rekognition', 'us-east-1')
bucket= 'smartdoorpictures'
FACE_LIST= ["andrew", "johnny", "katie"]
key_target= 'katie(testagainst).jpg'
threshold=0
RECOGNIZED_FACE = False
IS_FACE=False
region_name= 'us-east-1'
message = []
MIN_SIM= 60.0


if __name__ == "__main__":

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

    
    print(str.join(',', message))

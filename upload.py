#!/usr/bin/python3
import cgi
import os
import time
import cv2
import boto3
import time
ec2 = boto3.resource('ec2' , region_name = 'ap-south-1')

from cvzone.HandTrackingModule import HandDetector
upload_dir = "myupload/"

print("Content-Type: text/plain")
print()

try:
    form = cgi.FieldStorage()
    image_file = form['image']
    
    if image_file.filename:
        timestamp = int(time.time())
#        filename = f"image_{timestamp}.png"
        filename = "myimage.png"
        
        filepath = os.path.join(upload_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(image_file.file.read())
        print("<p>Live Streaming Started ..</p>")
    else:
        print("No image file received")
except Exception as e:
    print("An error occurred:", str(e))

def LaunchOS():
    instances = ec2.create_instances(
        ImageId="ami-0da59f1af71ea4ad2",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
      #  SecurityGroupIds=[
      #  'sg-0072cb1b72ca4eeaf',
   # ],
    )
    print("os launched ...")
detector = HandDetector(maxHands=1,
                        detectionCon=0.8)

img = cv2.imread("myupload/myimage.png")

hand = detector.findHands(img , draw=False)
if hand:
        lmlist = hand[0]
        if lmlist:
            fingerup = detector.fingersUp(lmlist)
            print(fingerup)
            if fingerup == [0, 1, 0, 0, 0]:
                print("index finger ..")
                LaunchOS()

            elif fingerup == [0, 1, 1, 0, 0]:
                print("index and middle finger ..")

            else:
                print("i work with index or middle finger ..")

else:
        print("no hand detected")
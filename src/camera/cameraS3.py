import time
import subprocess
from datetime import datetime, timedelta
import boto3 # type: ignore
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient  # type: ignore
import json
import os

def delete_expired_local_image(folder, retention_time):
    current_time = datetime.now()
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if current_time - creation_time > retention_time:
                os.remove(file_path)
                print(f"Deleted expired file: {file_name}")


def capture_image_and_upload():
    myMQTTClient = AWSIoTMQTTClient("raspberryPi")
    myMQTTClient.configureEndpoint("a18pydta3rp3tt-ats.iot.eu-north-1.amazonaws.com", 8883)
    myMQTTClient.configureCredentials("/home/group4/certs/AmazonRootCA1.pem", 
                                    "/home/group4/certs/private.pem.key",
                                    "/home/group4/certs/certificate.pem.crt")
    local_storage = "/home/group4/images"

    try:
        myMQTTClient.configureOfflinePublishQueueing(-1)
        myMQTTClient.configureDrainingFrequency(2)
        myMQTTClient.configureConnectDisconnectTimeout(30)
        myMQTTClient.configureMQTTOperationTimeout(20)
        print('Initiating Realtime Data Transfer From Raspberry Pi')

        s3_client = boto3.client('s3')
        s3_bucket = "myiotimagesbucket"

        topic = "images/notifications"

        myMQTTClient.connect()
        print("Connected to AWS IoT Core")

        retention_time = timedelta(minutes=30)
    except:
        print("Connection Failed. Image not sent.")

    while True:

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"{local_storage}/image_{timestamp}.jpg"
            try:

                subprocess.run(["libcamera-still", "-o", file_path])
                print(f"Image saved to {file_path}")

                s3_key = f"images/photo_{timestamp}.jpg"
                s3_client.upload_file(file_path, s3_bucket, s3_key)
                print(f"Uploaded {file_path} to S3 as {s3_key}")

                message = {"bucket": s3_bucket,
                        "key": s3_key,
                        "timestamp": timestamp}
                
                myMQTTClient.publish(topic, json.dumps(message), 1)
                print("Published notification to AWS IoT Core")

                delete_expired_local_image(local_storage, retention_time)
            except Exception as e:
                print(f"Error:{e}")

            return file_path

""" try:
    while True:
        capture_image_and_upload()
        time.sleep(10)
except KeyboardInterrupt:
    print("images capturing stopped.") """
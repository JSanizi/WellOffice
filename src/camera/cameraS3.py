import time
import subprocess
from datetime import datetime
import boto3 # type: ignore
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient  # type: ignore
import json



def capture_image_and_upload():
    myMQTTClient = AWSIoTMQTTClient("raspberryPi")
    myMQTTClient.configureEndpoint("a18pydta3rp3tt-ats.iot.eu-north-1.amazonaws.com", 8883)
    myMQTTClient.configureCredentials("/home/group4/certs/AmazonRootCA1.pem", 
                                    "/home/group4/certs/private.pem.key",
                                    "/home/group4/certs/certificate.pem.crt")

    myMQTTClient.configureOfflinePublishQueueing(-1)
    myMQTTClient.configureDrainingFrequency(2)
    myMQTTClient.configureConnectDisconnectTimeout(10)
    myMQTTClient.configureMQTTOperationTimeout(5)
    print('Initiating Realtime Data Transfer From Raspberry Pi')

    s3_client = boto3.client('s3')
    s3_bucket = "myiotimagesbucket"

    topic = "images/notifications"

    myMQTTClient.connect()
    print("Connected to AWS IoT Core")

    local_storage = "/home/group4/images"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"{local_storage}/image_{timestamp}.jpg"

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

    return file_path

""" try:
    while True:
        capture_image_and_upload()
        time.sleep(10)
except KeyboardInterrupt:
    print("images capturing stopped.") """
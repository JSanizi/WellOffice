import time
import requests
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient  # type: ignore
import json
from config import DeconzAPI
from lightbulb.light_control import Controller
from lightbulb.lightbulbs import Lightbulb

def handle_mqtt_message(client, userdata, message):
    payload = json.loads(message.payload)

    light_id = payload.get("light_id")
    brightness = payload.get("brightness")
    temperature = payload.get("temperature")

    if light_id is None:
        print("No light_id specified in the message.")
        return
    
    if brightness is not None:
        Controller.set_light_brightness(api_url, light_id, brightness)
    if temperature is not None:
        Controller.set_light_temperature(api_url, light_id, temperature)

def main():
    # Instantiate the DeconzAPI class with the IP address of your deCONZ device
    deconz = DeconzAPI(deconz_ip="172.30.212.135")
    global api_url
    api_url = deconz.get_api_url()
    lightbulbs = Lightbulb.list_of_paired_lightbulbs(url=api_url)

    if not lightbulbs:
        print("No lightbulbs found.")
        return
    
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

    topic = "bulbs/control"

    myMQTTClient.connect()
    print("Connected to AWS IoT Core")

    myMQTTClient.subscribe(topic,1,handle_mqtt_message)
    print(f"Subscribed to topic: {topic}")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Exiting...")
        myMQTTClient.disconnect()


if __name__ == "__main__":
    main()
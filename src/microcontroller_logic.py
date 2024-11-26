""" When Raspberry Pi turn on:
- Get APIKEY (Manually send from Phosocon)

Calibrate Light (Coordinating) 
- Turn off all lights registered in the system. 
- Turn on Light Bulb one.
- Capture Picture
- Forward picture and light id to the Cloud
- When coordinates are saved in the cloud, Turn off all lights
- Turn on Light bulb Two
- Capture picture
- Forward picture to Cloud and light ID
- When coordinates are saved in the cloud. Turn off all lights. 
- Turn on Light Bulb three
- Captures picture
- Forward picture and light ID to cloud
Note to Janice: Tjek om du kan gennem gå alle light_id i listen, uafhængigt af hvor mange der er. 


When all light bulb is calibrated:
While system is on and calibration is true:
- Set camera to take picture every ten seconds.
- Forward picture to cloud.
This is done until the system is turned off

If commands received from cloud. 
- Get command from cloud (mostly a Json request or something)
    - Light ID and what to do with the light ID's
- Send commands to lights
If not, wait for it."""

import time

from config import DeconzAPI
from lightbulb.light_control import Controller
from lightbulb.lightbulbs import Lightbulb
from camera.cameraS3 import capture_image_and_upload


def main():
    deconz = DeconzAPI(deconz_ip="172.30.212.135")
    api_url = deconz.get_api_url()

    # Turn off all lights registered in the system
    for lights in Lightbulb.list_of_paired_lightbulbs(url=api_url):
        Controller.turn_light_off(api_url, lights)
    time.sleep(2)
    
    for lights in Lightbulb.list_of_paired_lightbulbs(url=api_url):
        # Turn on the first light bulb and capture a picture
        Controller.turn_light_on(api_url, lights)
        # Capture picture
        capture_image_and_upload()
        Controller.turn_light_off(api_url,lights)
        time.sleep(2)

    print("Calibration done - Welloffice is now running")

    while True:
        # Set camera to take a picture every ten seconds and forward the picture to the cloud
        capture_image_and_upload()
        time.sleep(10)

    # Raspberry Pi will receive message from the cloud.
    # First we initiate which the light bulb that is closest, futhers and in the middle received from the cloud
    futherst_light = "furtherest lightbulb: light_id"
    closest_light = "closest lighbulb: light_id"
    middle_light = "moddile lightbulb: light_id"

    # We receive a message about the human activity in the room.

    if message == "Person not in the room":
        Controller.set_light_turn_on(api_url, lights)
        Controller.set_light_brightness(api_url, lights, 15)
    else:
        Controller.set_light_turn_on(api_url, lights)
        Controller.set_light_brightness(api_url, lights, 85)
        Controller.set_light_temperature(api_url, lights, 3500)
        if message == "Person is relaxed":
            Controller-set_light_brightness(api_url, closest_light, 75)
            Controller.set_light_brightness(api_url, futherst_light, 25)
            Controller.set_light_brightness(api_url, middle_light, 25)
            Controller.set_light_temperature(api_url, lights, 2700)
        else:    
            Controller.set_light_brightness(api_url, closest_lights, 100)
            Controller.set_light_brightness(api_url, furtherst_lights, 40)
            Controller.set_light_brightness(api_url, middle_lights, 40)
            Controller.set_light_temperature(api_url, lights, 4300)
 
    

if __name__ == "__main__":
    main()

# The Raspberry Pi will then calibrate the light by turning off all lights registered in the system.
# It will then turn on the first light bulb and capture a picture.
# The picture and light ID will be forwarded to the cloud.
# When the coordinates are saved in the cloud, all lights will be turned off.
# The second light bulb will be turned on, and a picture will be captured.
# The picture will be forwarded to the cloud along with the light ID.
# When the coordinates are saved in the cloud, all lights will be turned off.
# The third light bulb will be turned on, and a picture will be captured.
# The picture and light ID will be forwarded to the cloud.
# When the coordinates are saved in the cloud, all lights will be turned off.
# The Raspberry Pi will then set the camera to take a picture every ten seconds and forward the picture to the cloud.
# This will continue until the system is turned off.
# If commands are received from the cloud, the Raspberry Pi will get the command from the cloud, which is mostly a JSON request.
# The Raspberry Pi will get the light ID and what to do with the light IDs.
# The Raspberry Pi will then send the commands to the lights.
# If no commands are received, the Raspberry Pi will wait for it.

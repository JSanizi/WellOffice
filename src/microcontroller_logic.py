import time
import json
from config import DeconzAPI
from lightbulb.light_control import Controller
from lightbulb.lightbulbs import Lightbulb
from camera.cameraS3 import capture_image_and_upload
import lightbulbs_model as lb
import human_model as har
import euclidian_process as ep

def main():
    json_path = "/home/group4/Desktop/P5_Prototype1/src/lightbulbslogic.json"
    deconz = DeconzAPI(deconz_ip="172.17.202.226")
    api_url = deconz.get_api_url()
    lights = Lightbulb.list_of_paired_lightbulbs(url=api_url)

    # Turn off all lights registered in the system
    for light in lights:
        Controller.turn_light_off(api_url, light)
    time.sleep(2)
    
    for light in lights:
        detected = False
        while not detected:  # Retry until 'lightbulbOn' is detected
            # Turn on the first light bulb and capture a picture
            Controller.turn_light_on(api_url, light)
            Controller.set_light_brightness(api_url, light, 100)
            Controller.set_light_temperature(api_url, light, 3500)
            
            # Capture picture
            auxImage = capture_image_and_upload()
            
            # Detect light bulb that's on
            light_detected = lb.infere(auxImage, light)
            
            # If a lightbulb with the class 'lightbulbOn' is detected, move to the next light
            if light_detected:  # Modify infere to return a boolean
                break  # Exit the retry loop and move to the next light bulb
            
            if not detected:
                print("No 'lightbulbOn' detected. Retrying...")
                time.sleep(2)
        
        # Turn off the current light bulb before moving to the next
        Controller.turn_light_off(api_url, light)
        time.sleep(2)

    print("Calibration done - Welloffice is now running")
	
    # Turn on all lights registered in the system
    for light in lights:
        Controller.turn_light_on(api_url, light)
    time.sleep(2)

    while True:
        # Set camera to take a picture every ten seconds and forward the picture to the cloud
        human_image = capture_image_and_upload()
        har.human_inference(human_image)
        ep.update_euclidean_order(json_path)

        try:
            with open(json_path, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            print("JSON file was not found. Creating a new one.")
            data = {
                "light_bulbs": [],
                "human_activity": "",
                "human_coordinates": {"x": None, "y": None},
                "closest_light": None,
                "middle_light": None,
                "furthest_light": None
            }

        human_activity = data["human_activity"]
        closest_light = data["closest_light"]
        middle_light = data["middle_light"]
        furthest_light = data["furthest_light"]

        if human_activity == "No human detected":
            for light in lights:
                Controller.turn_light_on(api_url, light)
                Controller.set_light_temperature(api_url, light, 3500)
                Controller.set_light_brightness(api_url, light, 15)
        elif human_activity == "default":
            for light in lights:
                Controller.turn_light_on(api_url, light)
                Controller.set_light_brightness(api_url, light, 85)
                Controller.set_light_temperature(api_url, light, 3500)
        elif human_activity == "relaxed":
            Controller.set_light_brightness(api_url, closest_light, 85)
            Controller.set_light_brightness(api_url, furthest_light, 25)
            Controller.set_light_brightness(api_url, middle_light, 15)
            for light in lights:
                Controller.set_light_temperature(api_url, light, 2700)
        elif human_activity == "focused":    
            Controller.set_light_brightness(api_url, closest_light, 100)
            Controller.set_light_brightness(api_url, furthest_light, 30)
            Controller.set_light_brightness(api_url, middle_light, 15)
            for light in lights:
                Controller.set_light_temperature(api_url, light, 4300)
        else:
            print("The human activity is not recognized.")

        time.sleep(5)

if __name__ == "__main__":
    main()

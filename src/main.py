import time
import requests

from config import DeconzAPI
from lightbulb import Lightbulb
from light_control import Controller

def main():
    # Instantiate the DeconzAPI class with the IP address of your deCONZ device
    deconz = DeconzAPI(deconz_ip="172.24.112.1")
    api_url = deconz.get_api_url()
    lightbulbs = Lightbulb.list_of_paired_lightbulbs(url=api_url)

    if lightbulbs:
        Controller.turn_light_on(api_url, 3)
        Controller.set_light_brightness(api_url, 3, 40)
        Controller.set_light_temperature(api_url, 3, 4300)

    else:
        print("No lightbulbs found.")

if __name__ == "__main__":
    main()
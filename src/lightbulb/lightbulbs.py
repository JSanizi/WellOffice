import requests
import json

from config import DeconzAPI

class Lightbulb:
    def __init__(self):
        self.url = DeconzAPI.get_api_url()
        self.lights = self.list_of_paired_lightbulbs(self.url)

    def list_of_paired_lightbulbs(url):
        """Discover all the available lights in the deCONZ network."""
        response = requests.get(f"{url}/lights")

        if response.status_code == 200:
            lights = response.json()
            # print("List of lights:", lights)
            return lights
        else:
            print(f"Failed to discover lights: {response.status_code}")
            return None
    
def check_for_new_lights(self):
    """Check if any new lights are available for pairing."""
    api_url = self.get_api_url()

    if api_url:
        print("Checking for new lights...")
        # Send a GET request to check the available lights
        response = requests.get(f"{api_url}/lights")
        
        if response.status_code == 200:
            lights = response.json()
            if lights:
                #print(f"Found lights: {lights}")
                return lights  # Return the dictionary of found lights with their light IDs
            else:
                print("No new lights found.")
                return None
        else:
            print(f"Failed to retrieve lights: {response.status_code}, {response.json()}")
            return None
    else:
        print("API URL not available.")
        return None    
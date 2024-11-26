import requests

from config import DeconzAPI

class Controller:
    def __init__(self, api_url):
        self.api_url = api_url

    def turn_light_on(api_url, light_id):
        # Check if the light is already on
        if Controller.check_light_state(api_url, light_id):
            # print(f"Light {light_id} is already on.")
            return # Exit the function if the light is already on
        else:
            payload = {"on": True}  # Turn the light on
            response = requests.put(f"{api_url}/lights/{light_id}/state", json=payload)
            if response.status_code == 200:
                print(f"Turning Light {light_id} on...")
            else:
                print(f"Failed to turn on light {light_id}.")


    def turn_light_off(api_url, light_id):
        # Check if the light is already off
        if Controller.check_light_state(api_url, light_id):
            # print(f"Light {light_id} is already off.")
            return # Exit the function if the light is already off
        else:
            payload = {"on": False}  # Turn the light off
            response = requests.put(f"{api_url}/lights/{light_id}/state", json=payload)
            if response.status_code == 200:
                print(f"Turning Light {light_id} off...")
            else:
                print(f"Failed to turn off light {light_id}.")


    def set_light_brightness(api_url, light_id, percentage):
        brightness = (percentage / 100) * 254  # Convert percentage to 0-254 scale
        
        payload = {"bri": brightness}  # Set brightness value
        response = requests.put(f"{api_url}/lights/{light_id}/state", json=payload)
        if response.status_code == 200:
            print(f"Setting light {light_id} brightness {brightness}...")
        else:
            print(f"Failed to set brightness for light {light_id}.")

    
    def set_light_temperature(api_url, light_id, temperature):
        temperature = Controller.kelvin_to_ct(temperature)  # Convert Kelvin to CT value

        """Set the light temperature (color temperature)."""
        url = f"{api_url}/lights/{light_id}/state"
        payload = {"ct": temperature}  # Color temperature value 
        response = requests.put(url, json=payload)
        
        if response.status_code == 200:
            print(f"Setting Light {light_id} to light temperature {temperature}.")
        else:
            print(f"Failed to set light {light_id} temperature: {response.status_code} - {response.text}")

    def kelvin_to_ct(kelvin):
        """
        Convert Kelvin temperature to deCONZ color temperature (CT) value.
        Kelvin range: 2200K (warm light) to 6500K (cool daylight)
        CT range: 500 (warmest) to 153 (coolest)
        """
        # Ensure the Kelvin temperature is within the supported range
        if kelvin < 2200 or kelvin > 6500:
            print("Kelvin temperature must be between 2200K and 6500K.")
            return None

        # Linear conversion from Kelvin to CT
        ct_value = 500 - ((kelvin - 2200) / (6500 - 2200)) * (500 - 153)
        return round(ct_value)

    def check_light_state(api_url, light_id):
        """Check the state of a specific light and print details."""
        url = f"{api_url}/lights/{light_id}"  # API endpoint for light state
        response = requests.get(url)

        if response.status_code == 200:
            state = response.json()  # Parse the JSON response
            
            """# Extract the light's state
            is_on = state["state"]["on"]
            brightness = state["state"]["bri"]
            light_temperature = state["state"]["ct"]

            # Print the current state of the light
            if is_on:
                print(f"Light {light_id} is ON.")
            else:
                print(f"Light {light_id} is OFF.")
            
            print(f"Brightness: {brightness} (0-254 scale)")
            print(f"Light Temperature: {light_temperature} (Range: 153-500)")"""
        else:
            print(f"Failed to retrieve state for light {light_id}: {response.status_code}")
        
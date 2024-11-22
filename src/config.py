import requests
import time

class DeconzAPI:
    def __init__(self, deconz_ip, api_port="8080"):
        self.deconz_ip = deconz_ip
        self.api_port = api_port
        self.api_key = None
        self.api_url = None
    
    def get_api_key(self):
        """Get the API key from the deCONZ device."""
        url = f"http://{self.deconz_ip}:{self.api_port}/api"
        response = requests.post(url, json={"devicetype": "my_python_app"})

        if response.status_code == 200:
            self.api_key = response.json()[0]["success"]["username"]
            # print("API Key:", self.api_key)
        else:
            print("Failed to get API Key:", response.json())
            self.api_key = None
    
    def create_api_url(self):
        """Get the full API URL using the API key."""
        if not self.api_key:
            print("API key not set. Fetching the key first...")
            self.get_api_key()  # Get the API key if it hasn't been retrieved yet
        if self.api_key:
            return f"http://{self.deconz_ip}:{self.api_port}/api/{self.api_key}"
        else:
            return None
    
    def get_api_url(self):
        """Get the full API URL using the API key."""
        while not self.api_url:
            self.api_url = self.create_api_url()
            if not self.api_url:
                print("Failed to retrieve the API URL. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                #print("API URL:", self.api_url)
                return self.api_url

# Importar librerías necesarias
from inference_sdk import InferenceHTTPClient
import cv2
import json

# Client Initialization
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="adQagzOCzh8qIHWuFBhz"
)

# Path of the JSON file
json_path = "/home/group4/Desktop/P5_Prototype1/src/lightbulbslogic.json"
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

def infere(inferedImage, lightID):
    # Make an inference request
    result = CLIENT.infer(inferedImage, model_id="lightbulb-pq5iq/2")

    # Load the image
    image = cv2.imread(inferedImage)

    # Check if the image was loaded correctly
    if image is None:
        print("The image was not loaded.")
        return False
    else:
        if result:
            predictions = result.get("predictions", [])
            detected_on = False

            if predictions:
                # Iterate over the predictions
                for i, pred in enumerate(predictions):
                    x = int(pred.get("x"))
                    y = int(pred.get("y"))
                    width = int(pred.get("width"))
                    height = int(pred.get("height"))
                    class_name = pred.get("class")
                    confidence = pred.get("confidence")

                    print(f"Detection {i + 1}: {class_name} (confidence: {confidence:.2f})")

                    # Process lightbulb detections
                    if class_name in ["lightbulbOn", "lightbulbOff"]:
                        # Check if the lightbulb already exists in the JSON
                        existing_light = next(
                            (light for light in data["light_bulbs"] if light["ID"] == lightID), None
                        )

                        if existing_light:
                            # Update coordinates only
                            existing_light["x"] = x
                            existing_light["y"] = y
                            print(f"Updating the JSON: {existing_light}")
                        else:
                            if len(data["light_bulbs"]) < 3:
                                # Add new lightbulb to JSON
                                new_lightbulb = {"x": x, "y": y, "ID": lightID}
                                data["light_bulbs"].append(new_lightbulb)
                                print(f"Added lightbulb to JSON: {new_lightbulb}")
                        
                    # Detect lightbulbOn
                    if class_name == "lightbulbOn":
                        detected_on = True

                    # Draw a rectangle around the detected object
                    top_left = (x - width // 2, y - height // 2)
                    bottom_right = (x + width // 2, y + height // 2)

                    # Draw the rectangle
                    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

                    # Add a label with the class name and confidence
                    label = f"{class_name} ({confidence:.2f})"
                    cv2.putText(image, label, (top_left[0], top_left[1] - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Display the image with the detections
                with open(json_path, "w") as json_file:
                    json.dump(data, json_file, indent=4)
                print(f"JSON updated stored in: {json_path}")

                return detected_on
            
            print("No 'lightbulbOn' detected in predictions.")
            return False  # No valid predictions
        else:
            print("No results were returned.")
            return False  # No results
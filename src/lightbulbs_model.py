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
json_path = "lightbulbslogic.json"
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
    else:
        if result:
            predictions = result.get("predictions", [])

            if predictions:
                # Iterate over the predictions
                for i, pred in enumerate(predictions):
                    x = int(pred.get("x"))
                    y = int(pred.get("y"))
                    width = int(pred.get("width"))
                    height = int(pred.get("height"))
                    class_name = pred.get("class")
                    confidence = pred.get("confidence")

                    # Print the detection details
                    print(f"Detection {i + 1}:")
                    print(f"  Coordinates: (x={x}, y={y})")
                    print(f"  Size: (width={width}, height={height})")
                    print(f"  Class Name: {class_name}")
                    print(f"  Confidence: {confidence:.2f}")

                    # If the class is "lightbulbOn", add to the JSON
                    if class_name == "lightbulbOn":
                        # Verify if the light bulb is already in the JSON
                        existing_light = next((light for light in data["light_bulbs"] if light["ID"] == lightID), None)

                        if existing_light:
                            # If the light bulb is already in the JSON, update only its coordinates
                            existing_light["x"] = x
                            existing_light["y"] = y
                            print(f"Updating the JSON: {existing_light}")
                        else:
                            if len(data["light_bulbs"]) >= 3:
                                print(f"There are only 3 light bulbs allowed.")
                            else:
                                # If the light bulb is not in the JSON, add it
                                new_lightbulb = {"x": x, "y": y, "ID": lightID}
                                # Add the new light bulb to the JSON
                                data["light_bulbs"].append(new_lightbulb)
                                print(f"Adding to JSON: {new_lightbulb}")

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
            else:
                print("No predictions were found.")
        else:
            print("No results were returned.")
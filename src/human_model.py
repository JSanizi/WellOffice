import json
from ultralytics import YOLO
from PIL import Image, ImageDraw
from inference_sdk import InferenceHTTPClient

# Dictionary to map the numeric activity labels to human-readable strings
ACTIVITY_MAP = {
    0.0: "calling",
    1.0: "eating",
    2.0: "siting",
    3.0: "sleeping",
    4.0: "texting",
    5.0: "using_laptop",
    "default": "default",
    "No human detected": "No human detected"
}

# Function to annotate and save results
def annotate_and_save(image_path, detections, output_image_path):
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    for detection in detections:
        x_min, y_min, x_max, y_max = detection
        center_x = int((x_min + x_max) / 2)
        center_y = int((y_min + y_max) / 2)
        
        # Draw bounding box
        draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=3)
        
        # Draw center point
        radius = 20
        draw.ellipse(
            (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
            fill="blue",
            outline="blue",
        )

# Function to update the JSON file
def update_lightbulbs_logic(human_coordinates, activity):
    file_path = "/home/group4/Desktop/P5_Prototype1/src/lightbulbslogic.json"

    # Read the current JSON data
    with open(file_path, "r") as file:
        data = json.load(file)

    # Update human_coordinates
    data["human_coordinates"]["x"] = human_coordinates["x"]
    data["human_coordinates"]["y"] = human_coordinates["y"]

    # Convert numerical activity to string using ACTIVITY_MAP
    activity_label = ACTIVITY_MAP.get(activity)  # Default to "No human detected" if not in the map
    human_activity = ""

    if "calling" in activity_label or "texting" in activity_label or "using_laptop" in activity_label:
        human_activity = "focused"
    elif "eating" in activity_label or "siting" in activity_label or "sleeping" in activity_label:
        human_activity = "relaxed"
    elif "default" in activity_label:
        human_activity = "default"
    else:
        human_activity = "No human detected"

    data["human_activity"] = human_activity

    # Write updated data back to the file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Updated lightbulbslogic.json with coordinates and activity.")

def human_inference(aux_image):
    # Image path
    input_image_path = aux_image

    # Run YOLO inference
    yolo_results = yolo_model([input_image_path])
    yolo_detections = []
    activity = None
    highest_confidence = 0

    for result in yolo_results:
        if result.boxes is not None:
            for box in result.boxes:
                # Extract coordinates (xmin, ymin, xmax, ymax) and activity
                x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
                confidence = box.conf.tolist()[0]
                detected_activity = box.cls.tolist()[0]

                yolo_detections.append((x_min, y_min, x_max, y_max))

                if confidence > highest_confidence:
                    highest_confidence = confidence
                    activity = detected_activity # Activity label predicted by YOLO

    # Check if YOLO found any detections
    if yolo_detections:
        print("YOLO detected objects.")
        annotate_and_save(
            input_image_path,
            yolo_detections,
            "human_model_result.jpg"
        )
        # Get the center of the first detection
        first_detection = yolo_detections[0]
        human_center = {
            "x": int((first_detection[0] + first_detection[2]) / 2),
            "y": int((first_detection[1] + first_detection[3]) / 2)
        }
    elif not yolo_detections:
        print("YOLO did not detect any objects. Falling back to second model.")
        
        # Run inference on the backup model
        second_model_result = client.infer(input_image_path, model_id="person-detection-9a6mk/16")
        
        second_model_detections = []
        for pred in second_model_result["predictions"]: #Safely got the predictions
            # Extract bounding box coordinates
            x_min = pred["x"] - pred["width"] / 2
            y_min = pred["y"] - pred["height"] / 2
            x_max = pred["x"] + pred["width"] / 2
            y_max = pred["y"] + pred["height"] / 2
            second_model_detections.append((x_min, y_min, x_max, y_max))

        if second_model_detections:
            annotate_and_save(
                input_image_path,
                second_model_detections,
                "human_model_result.jpg"
            )
            # Get the center of the first detection
            first_detection = second_model_detections[0]
            human_center = {
                "x": int((first_detection[0] + first_detection[2]) / 2),
                "y": int((first_detection[1] + first_detection[3]) / 2)
            }
            activity = "default"  # No activity label from the second model
        else:
            print("Second model also did not detect any objects.")
            human_center = {"x": None, "y": None} # No coordinates found
            activity = "No human detected" # No activity because there was no human
    else:
        return

    # Update the JSON file with coordinates and activity
    update_lightbulbs_logic(human_center, activity)

# YOLO model initialization
yolo_model = YOLO("/home/group4/Desktop/P5_Prototype1/src/bestHAR.pt")

# Inference client initialization
client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="HBctR84K7sX66IDRBCCR"
)
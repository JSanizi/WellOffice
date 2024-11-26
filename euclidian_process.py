import json
import math

# Function to calculate Euclidean distance
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Function to update JSON with Euclidean distances order
def update_euclidean_order(json_file_path):
    # Read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    human_coordinates = data["human_coordinates"]
    light_bulbs = data["light_bulbs"]

    # Calculate distances and store along with their indices
    distances = []
    for index, bulb in enumerate(light_bulbs):
        distance = calculate_distance(
            human_coordinates["x"],
            human_coordinates["y"],
            bulb["x"],
            bulb["y"]
        )
        distances.append((index + 1, distance))  # Store 1-based index and distance

    # Sort distances by the second element (actual distance)
    sorted_distances = sorted(distances, key=lambda x: x[1])

    # Extract the order of the indices
    order = [item[0] for item in sorted_distances]

    # Update the JSON structure
    data["euclidian_lights"] = order

    # Write the updated JSON back to the file
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Updated {json_file_path} with Euclidean distances order: {order}")

# Path to the JSON file
json_file_path = "lightbulbslogic.json"

# Update the JSON with Euclidean distances order
update_euclidean_order(json_file_path)
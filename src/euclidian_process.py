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
    human_activity = data["human_activity"]

    if human_activity == "No human detected":
        data["closest_light"] = None
        data["middle_light"] = None
        data["furthest_light"] = None
    else:
        # Calculate distances and store along with their indices
        distances = []
        for bulb in light_bulbs:
            distance = calculate_distance(
                human_coordinates["x"] if human_coordinates["x"] is not None else 0,
                human_coordinates["y"] if human_coordinates["y"] is not None else 0,
                bulb["x"],
                bulb["y"]
            )
            distances.append({"ID": bulb["ID"], "distance": distance})

        # Sort distances by the second element (actual distance)
        sorted_distances = sorted(distances, key=lambda x: x["distance"])

        # Update the JSON structure with closest, middle, and furthest lights.
        if len(sorted_distances) >= 3:
            data["closest_light"] = sorted_distances[0]["ID"]
            data["middle_light"] = sorted_distances[1]["ID"]
            data["furthest_light"] = sorted_distances[2]["ID"]
        else:
            print("Not enough light bulbs to determine closest, middle, and furthest lights.")

        # Write the updated JSON back to the file
        with open(json_file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Updated {json_file_path} with closest, middle, and furthest lights.")
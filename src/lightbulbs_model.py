# Importar librerías necesarias
from inference_sdk import InferenceHTTPClient
import cv2
import json

# Inicializar el cliente
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="adQagzOCzh8qIHWuFBhz"
)

# Cargar el JSON inicial
json_path = "lightbulbslogic.json"
try:
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print("Archivo JSON no encontrado. Creando uno nuevo.")
    data = {
        "light_bulbs": [],
        "human_activity": "",
        "human_coordinates": {"x": None, "y": None},
        "euclidian_lights": []
    }

def infere(inferedImage, lightID):
    # Realizar la inferencia
    result = CLIENT.infer(inferedImage, model_id="lightbulb-pq5iq/2")

    # Cargar la imagen
    image = cv2.imread(inferedImage)

    if image is None:
        print("Error al cargar la imagen.")
    else:
        if result:
            predictions = result.get("predictions", [])

            if predictions:
                for i, pred in enumerate(predictions):
                    x = int(pred.get("x"))
                    y = int(pred.get("y"))
                    width = int(pred.get("width"))
                    height = int(pred.get("height"))
                    class_name = pred.get("class")
                    confidence = pred.get("confidence")

                    # Imprimir detalles de cada detección
                    print(f"Detección {i + 1}:")
                    print(f"  Coordenadas: (x={x}, y={y})")
                    print(f"  Tamaño: (ancho={width}, alto={height})")
                    print(f"  Clase: {class_name}")
                    print(f"  Confianza: {confidence:.2f}")

                    # Si la clase es "lightbulbOn", agregar al JSON
                    if class_name == "lightbulbOn":
                        new_lightbulb = {"x": x, "y": y, "ID": lightID}
                        # Insertar con el siguiente índice disponible
                        data["light_bulbs"].append(new_lightbulb)
                        print(f"Agregado al JSON: {new_lightbulb}")

                    # Calcular las esquinas del cuadro delimitador
                    top_left = (x - width // 2, y - height // 2)
                    bottom_right = (x + width // 2, y + height // 2)

                    # Dibujar el cuadro en la imagen
                    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

                    # Añadir texto con la clase y la confianza
                    label = f"{class_name} ({confidence:.2f})"
                    cv2.putText(image, label, (top_left[0], top_left[1] - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Guardar el JSON actualizado
                with open(json_path, "w") as json_file:
                    json.dump(data, json_file, indent=4)
                print(f"JSON actualizado guardado en: {json_path}")
            else:
                print("No se encontraron predicciones.")
        else:
            print("No se obtuvo ningún resultado.")



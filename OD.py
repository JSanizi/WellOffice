from ultralytics import YOLO
from PIL import Image

model = YOLO("runs/detect/train43/weights/last.pt")

# model.tune(data="datasets/HAR/data.yaml", epochs=20, iterations=10, optimizer="AdamW", plots=False, val=False, imgsz=320)


# results = model.train(data="datasets/HAR/data.yaml", epochs=20, batch=24, imgsz=320)

# metrics = model.val()  # no arguments needed, dataset and settings remembered
# metrics.box.map  # map50-95
# metrics.box.map50  # map50
# metrics.box.map75  # map75
# metrics.box.maps  # a list contains map50-95 of each category


image = Image.open("texting.jpg")
new_image = image.resize((320, 320))
new_image.save("texting320.jpg")


results = model(["texting320.jpg","laptop4_320.jpg", "laptop5_320.jpg" ,"laptop6_320.jpg", "laptop1_320.jpg", "me2.jpg", "me3.jpg", "janice.jpg"])  # return a list of Results objects


# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="result.jpg")  # save to disk


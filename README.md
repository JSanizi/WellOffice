# 💡 WellOffice - Enhancing Room Experience with Smart Lighting 
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-Academic-green.svg)
![Status](https://img.shields.io/badge/status-Completed-success.svg)

*An IoT-Based Smart Lighting System for Enhancing Focus and Relaxation in Office Spaces* 

**Authors:** Janice Sakina Akiza Nizigama, Tew Chuan Le, Eugenio Turcott Estrada, Gustavo Lucio Sepúlveda,   
**University:** Aalborg University Copenhagen  
**Supervisor:** Yan Kyaw Tun  
**Project Period:** Fall 2024 (E24 – IoT-based Systems and Architectures)  
**Repository:** [gusls02/P5_Prototype1#](https://github.com/gusls02/P5_Prototype1#) & forked ver. [JSanizi/WellOffice](https://github.com/JSanizi/WellOffice)  

## 🎥 Demo Video
[![Demo Video](https://img.youtube.com/vi/i-sr8tgOFAE/maxresdefault.jpg)](https://www.youtube.com/watch?v=i-sr8tgOFAE)

---

## 📖 Overview  

**WellOffice** is a smart lighting system designed to enhance **focus** and **relaxation** in a work office by adjusting the lighting based on human activity and presence.  
The project integrates **machine learning**, **IoT devices**, **cloud storage**, and **real-time adaptive lighting control** to deliver a personalized lighting environment.

According to research and system testing, lighting influences attention and comfort.  
WellOffice uses this insight to automatically adjust:

- **∼4300 K** for focus  
- **2700 K** for relaxation  
- **3500 K** as the default state  
- **15% brightness** when no one is in the room  

The system determines the user’s activity through camera input and adapts the light accordingly.

---

## 🧠 Project Architecture  

### System Components  

1. **Human Activity Recognition (HAR)**  
   - Implemented using pretrained PyTorch HAR models.  
   - Determines whether the user is in a relaxed or focused state.  
   - Models stored in `HAR_models/` and `src/lightbulb/bestHAR.pt`.  

2. **Camera & Cloud Integration**  
   - `src/camera/cameraS3.py`  
     - Captures images from the Raspberry Pi camera.  
     - Uploads captured images to **AWS S3** for further detection processing.  
   - S3 notifications are used to trigger the detection workflow.  

3. **Object Detection (Roboflow + YOLOv11)**  
   - The system sends images to Roboflow for:
     - Human detection  
     - Light bulb detection  
   - Roboflow returns bounding boxes and detection results.  

4. **Light Bulb Logic & Control**  
   Located in `src/lightbulb/`:
   - `human_model.py`  
     - Runs HAR inference to classify the user’s activity.  
   - `lightbulbs_model.py`  
     - Handles logic for interpreting detected light bulbs.  
   - `eulcidian_process.py`  
     - Calculates **Euclidean distances** between the detected human and each light bulb.  
     - Determines the bulb closest to the user.  
   - `microcontroller_logic.py`  
     - Applies lighting rules based on activity and distance.  
     - Sends commands to Philips Hue bulbs through a Zigbee gateway (e.g. ConBee II).  
   - `config.py`  
     - Configuration for paths, topics, device IDs etc.  
   - `lightbulbslogic.json`  
     - Stores light bulb positions, IDs, and behavior mappings.  
   - Default lighting behavior from the report:  
     - **Default mode:** 3500 K, 85% brightness  
     - **Relax mode:** 2700 K, 85% brightness  
     - **Focus mode:** 4300 K, 100% brightness  
     - **No-human mode:** 3500 K, 15% brightness  

5. **Configuration & Utilities**  
   - `src/config/datasetCleaner.py` – cleans and preprocesses datasets.  
   - `src/config/datasetIndexer.py` – indexes and structures datasets.  
   - `src/config/testMQTT.py` – verifies MQTT connectivity.  

6. **Test & Evaluation Images**  
   - `test_pictures/`  
     - Contains labelled images (e.g. `janice1computer.jpeg`, `gustavoworking.jpeg`, `lightbulb1on.jpeg`, `lightsoff.jpeg`)  
     - Used to validate detection performance and end-to-end logic.  

---

### Example Flow – From Detection to Light Control  

1. `cameraS3.py` captures an image and uploads it to S3 (or reads from `test_pictures/`).  
2. Roboflow performs object detection on the image:
   - Detects humans  
   - Detects light bulbs  
3. Detection results are sent back to the system.  
4. `eulcidian_process.py` computes which bulb is closest to the detected human.  
5. `human_model.py` classifies the user’s activity (focused, relaxed, idle).  
6. `microcontroller_logic.py` decides:
   - Which bulb(s) should turn on/off.  
   - What brightness and CCT to apply (e.g. ~4300 K for focused work, warmer for relaxation).  
7. Commands are sent to the smart lighting system (e.g. Philips Hue via Zigbee gateway).  

---

## ⚙️ Installation  

### Requirements  

- Python 3.10 or newer  
- Raspberry Pi 4 (recommended)  
- Raspberry Pi Camera Module  
- Philips Hue bulbs + compatible Zigbee gateway (e.g. ConBee II)  
- AWS account with an S3 bucket  
- MQTT broker (e.g. Mosquitto or AWS IoT Core)  

## 🚀 Usage

Below is an example of how to run the core scripts in sequence.

```bash
# 1️⃣ Test MQTT connectivity (optional)
python src/config/testMQTT.py

# 2️⃣ Run the camera module and upload images to AWS S3
python src/camera/cameraS3.py

# 3️⃣ Run the Human Activity Recognition model
python src/lightbulb/human_model.py

# 4️⃣ Compute Euclidean distances between humans and bulbs
python src/lightbulb/eulcidian_process.py

# 5️⃣ Execute the microcontroller logic to control the lights
python src/lightbulb/microcontroller_logic.py
```

You can also use the images in `test_pictures/` to validate how the models and logic behave without running the camera live.

---

## 📊 Evaluation & Results

The system is evaluated based on:

* ✅ **Detection performance** for humans and bulbs
* ✅ **Distance estimation quality** using Euclidean distance
* ✅ **Responsiveness** of the lighting system
* ✅ **Subjective user experience** in terms of focus/relaxation

From experiments and state-of-the-art research:

* The underlying object-detection approach (YOLO-based) achieved **high accuracy** in detecting humans and light bulbs.
* The lighting control algorithm (distance-based) maintained a reliable mapping between human position and the correct bulb being activated.
* User-oriented tests and literature showed that using **CCT ≈ 4300 K** for work tasks supports sustained attention, while warmer scenes (around **2700 K**) improved relaxation during breaks.

---

## 🧩 Repository Structure

```text
WellOffice/
├── .vscode/
│   └── settings.json
│
├── HAR_models/
│   ├── FullHARBest.pt
│   ├── FullHARLast.pt
│   └── NewBestHAR.pt
│
├── src/
│   ├── camera/
│   │   └── cameraS3.py
│   │
│   ├── config/
│   │   ├── datasetCleaner.py
│   │   ├── datasetIndexer.py
│   │   └── testMQTT.py
│   │
│   ├── lightbulb/
│   │   ├── bestHAR.pt
│   │   ├── config.py
│   │   ├── eulcidian_process.py
│   │   ├── human_model.py
│   │   ├── lightbulbs_model.py
│   │   ├── lightbulbslogic.json
│   │   └── microcontroller_logic.py
│
├── test_pictures/
│   ├── blankimage.jpg
│   ├── chuanle1computer.jpeg
│   ├── chuanledevouring.jpeg
│   ├── chuanlejanicecomputer.jpeg
│   ├── chuanlelights1.jpeg
│   ├── chuanlelights2.jpeg
│   ├── chuanleworkingtest.jpeg
│   ├── gustavolights.jpeg
│   ├── gustavoworking.jpeg
│   ├── human_model_result.jpg
│   ├── janice1computer.jpeg
│   ├── janice2computer.jpeg
│   ├── janicedoingnothing.jpeg
│   ├── janicelights.jpeg
│   ├── lightbulb1on.jpeg
│   ├── lightbulb2on.jpeg
│   ├── lightbulb3on.jpeg
│   ├── lightsoff.jpeg
│   └── lightson.jpeg
│
├── .gitattributes
└── README.md
```

---

## 📬 Contact
#### Janice Sakina Akiza Nizigama

🔗 LinkedIn: https://www.linkedin.com/in/janice-nizigama

💻 GitHub: https://github.com/JSanizi

#### Tew Chuan Le

🔗 LinkedIn: https://www.linkedin.com/in/chuan-le-tew-0209b4203/

#### Eugenio Turcott Estrada

🔗 LinkedIn: https://www.linkedin.com/in/eugenio-turcott/

💻 Github: https://github.com/eugenio-turcott

#### Gustavo Lucio Sepúlveda

🔗 LinkedIn: https://www.linkedin.com/in/gustavo-lucio-a65944259/

💻 Github: https://github.com/gusls02

---

## 🧾 License

© 2024 Aalborg University — Academic / Non-Commercial use permitted with citation.
For other uses, please contact the authors.

# NEW_GKLMOB_Busstop_object_detection

# Bus Stop Object Detection & Scoring – Klang Valley

This project focuses on detecting, classifying, and scoring bus stops across Klang Valley using computer vision and geospatial analysis. By combining object detection models, annotation workflows, and automated scoring logic, the project aims to support smart-city planning, public transport analysis, and infrastructure assessment.

The primary goals of this project are to:

* Automatically detect bus stops and related elements using computer vision.
* Classify various bus stop components (e.g., shelter, street light, rubbish bin, signage, etc.).
* Quantify the quality of each bus stop using a presence-based scoring system.
* Generate a reproducible pipeline for processing labels, aggregating object counts, computing scores, and visualizing results.
* Produce an interactive map for exploration and spatial analysis.

---

## 🔄 Workflow Overview
Below is the complete processing flow from annotation → scoring → map visualisation:


### **❗Pre-Requisite Installation**
Before continuing, install all required dependencies by running the following command in the terminal:

```
pip install -r requirements.txt
```

All scripts and notebooks assume the required packages are installed beforehand.


### **1. Image Annotation**

Images were annotated with the assistance of a custom model trained on **Roboflow**.
The model was used to pre-label bus-stop-related objects, and all annotations were manually verified.

#### **❗Annotation Methodology Disclaimer**
Annotations were generated using a Roboflow-trained model with label assist and human intervention. Because manual corrections were applied, the dataset is not perfectly reproducible. The model is actively being improved and is approaching reliability for autonomous annotation.

### **2. Export YOLOv8 Labels**

The annotated dataset source can be viewed and downloaded from the following Roboflow Universe link:  
https://universe.roboflow.com/anatomy-of-bus-stops-v2/busstop-detection-vldmg/dataset/21

Annotated images were exported in **YOLOv8 format** and downloaded to the local machine. This export automatically generated the following directory structure:

- `images/`  
- `labels/`  
- `data.yaml`  

The `data.yaml` file was extracted and placed at the top level of the repository. This file contains the **class index-to-name mapping** used during annotation and model training.  
This mapping is required later to correctly interpret YOLO label files and to identify which object class is present when recording object presence at each bus stop.

#### **⚠️ YOLOv8 File Format Disclaimer**

YOLOv8 was used **only as an annotation export format** to obtain structured text files containing bounding box information.  
The YOLOv8 model itself was **not used for training**. All model training and inference were performed using the **RF-DETR** models.

---

### **3. Label Extraction**

All YOLOv8 label files were extracted from the `labels/` directory and consolidated into a single file:

```
results_labels.yolov8
```

❗ **Key addition:**
The `data.yaml` file was also extracted at this stage and stored for reference.
It was used by later scripts to correctly translate YOLO class IDs into class names when recording object presence and counting objects at each bus stop.

### **4. Counting Objects per Bus Stop**

The script below iterates through all labels and aggregates object counts per bus stop:

```
aggregate_across_busstop/1_count_busstop_objects.py
```

Output: A structured table storing counts of each detected object for every bus stop.

### **5. Scoring Each Bus Stop**

Next, a presence-based scoring system was applied:

```
aggregate_across_busstop/2_calc_score.py
```

Each bus stop is assigned a score based on whether key elements (shelter, bench, lighting, etc.) are present.
*Note: Scores are presence-only; object quantity does not affect scoring.*

### **6. Merging Scores with Bus Stop Coordinates**

To prepare the dataset for mapping, detection scores were merged with the geographic coordinates of each bus stop:

```
map_based_visual/3_compile_score_and_coord.py
```

### **7. Point Map Visualisation Using Folium**

A point-based colour-graded map was generated via:

```
map_based_visual/4_create_point_map.py
```

The resulting Folium map displays each bus stop with a colour scale representing its quality score.

Links to both map visualisations are attached at the bottom of this document.

---

### **8. Hexagonal Grid Map Visualisation Using h3**

A hexagonal grid map was generated via:

```
map_based_visual/4b_create_h3_map.py
```

The resulting Folium map displays each bus stop area as a hexagonal cell with the same colour scale as the point map representing its quality score.

---

## 📦 Project Structure

```
GKLMOB_Busstop_object_detection/
│
├── aggregate_across_busstop/
│   ├── 1_count_busstop_objects.py
│   └── 2_calc_score.py
│
├── map_based_visual/
│   ├── 3_compile_score_and_coord.py
│   ├── 4_create_point_map.py
│   └── 4b_create_h3_map.py
│
├── results_labels.yolov8
├── data.yaml
└── README.md

```

---

## 🗺️ Output

* Aggregated object counts for each bus stop
* Presence-based infrastructure score
* Final dataset combining coordinates + scores
* An interactive point map and hexagonal map for exploration and decision-making

---

## 🚀 Future Improvements

* Introduce weighting to improve quality score accuracy
* Use more robust detection models for harder objects
* Add clustering or hotspot analysis

---

## Links to Map Visualisations (Hosted on Vercel)
* 1. Point Map Visualisation: [point map vis](https://new-gklmob-busstop-object-detection-three.vercel.app/)
* 2. H3 Map Visualitation: [h3 map vis](https://new-gklmob-busstop-object-detection-pi.vercel.app/)

---

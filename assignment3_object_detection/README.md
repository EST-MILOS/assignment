# Assignment 3 - Object Detection

## What this submission does

`your-detection.py` runs object detection on one or more images.  For every
detected object it prints the fields required by Assignment 3:

- `ClassID`, class name, and confidence
- `Left`, `Top`, `Right`, and `Bottom`
- `Width`, `Height`, `Area`, and `Center`

It also saves an annotated image with `Type`, confidence, `L`, `T`, `W`, `H`,
and `Area` drawn beside each bounding box.

## Run on the Jetson

For the Lecture 4 fruit model:

```bash
python3 your-detection.py fruit_2.jpg fruit_5.jpg \
  --model=ssd-mobilenet.onnx \
  --labels=labels.txt \
  --output-dir=assignment3_results \
  --threshold=0.30
```

For an installed Jetson model, such as the general COCO model:

```bash
python3 your-detection.py input.jpg \
  --network=ssd-mobilenet-v2 \
  --output-dir=results \
  --threshold=0.30
```

## Included evidence

- `results/fruit_2_detected.jpg` - strawberry detections
- `results/fruit_5_detected.jpg` - banana-scene detections
- `submission/Assignment3_Object_Detection_Report.pdf` - submission report

The report records the actual model outputs, including the Apple false-positive
in the banana image.

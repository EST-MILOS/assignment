#!/usr/bin/env python3
"""Detect objects in one or more images and print Assignment 3 measurements.

Run this on the Jetson after copying it there.  The model options are explicit
so the same script can be used with the fruit model exported in Lecture 4.
"""

import argparse
from pathlib import Path

import cv2
from jetson_inference import detectNet
from jetson_utils import videoOutput, videoSource


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run a custom SSD detector on images and report bounding-box measurements."
    )
    parser.add_argument("images", nargs="+", help="one or more input image paths")
    model_source = parser.add_mutually_exclusive_group(required=True)
    model_source.add_argument("--network", help="built-in Jetson model, for example ssd-mobilenet-v2")
    model_source.add_argument("--model", help="path to a custom exported ONNX model")
    parser.add_argument("--labels", help="class-label text file (required with --model)")
    parser.add_argument("--output-dir", required=True, help="folder for annotated result images")
    parser.add_argument("--threshold", type=float, default=0.30, help="minimum confidence")
    parser.add_argument("--overlay", default="box,labels,conf", help="drawing options for result images")
    return parser.parse_args()


def measure_detection(detection, class_name):
    """Collect the exact Assignment 3 fields, expressed in pixels."""
    left, top = float(detection.Left), float(detection.Top)
    right, bottom = float(detection.Right), float(detection.Bottom)
    width, height = right - left, bottom - top
    center_x, center_y = left + width / 2, top + height / 2

    return {
        "class_id": detection.ClassID,
        "class_name": class_name,
        "confidence": float(detection.Confidence),
        "left": left,
        "top": top,
        "right": right,
        "bottom": bottom,
        "width": width,
        "height": height,
        "area": width * height,
        "center_x": center_x,
        "center_y": center_y,
    }


def describe_detection(measurement):
    return (
        f"ClassID={measurement['class_id']}; ClassName={measurement['class_name']}; "
        f"Confidence={measurement['confidence']:.4f}; "
        f"Left={measurement['left']:.1f}; Top={measurement['top']:.1f}; "
        f"Right={measurement['right']:.1f}; Bottom={measurement['bottom']:.1f}; "
        f"Width={measurement['width']:.1f}; Height={measurement['height']:.1f}; "
        f"Area={measurement['area']:.1f}; "
        f"Center=({measurement['center_x']:.1f}, {measurement['center_y']:.1f})"
    )


def draw_assignment_labels(image_path, measurements):
    """Add the detailed field labels required in the Assignment 3 screenshots."""
    image = cv2.imread(str(image_path))
    if image is None:
        raise RuntimeError(f"Could not open the saved result image: {image_path}")

    for item in measurements:
        left, top = int(item["left"]), int(item["top"])
        right, bottom = int(item["right"]), int(item["bottom"])
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

        line_one = f"Type: {item['class_name']} {item['confidence'] * 100:.1f}%"
        line_two = (
            f"L:{left} T:{top} W:{int(item['width'])} "
            f"H:{int(item['height'])} Area:{int(item['area'])}"
        )
        text_y = max(36, top - 8)
        for line_number, text in enumerate((line_one, line_two)):
            y = text_y + line_number * 19
            cv2.putText(image, text, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(image, text, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)

    if not cv2.imwrite(str(image_path), image):
        raise RuntimeError(f"Could not write annotated result image: {image_path}")


def main():
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.network:
        net = detectNet(args.network, threshold=args.threshold)
        labels = None
    else:
        if not args.labels:
            raise ValueError("--labels is required when loading a custom --model")
        with open(args.labels, encoding="utf-8") as label_file:
            labels = [line.strip() for line in label_file if line.strip()]
        net = detectNet(
            model=args.model,
            labels=args.labels,
            input_blob="input_0",
            output_cvg="scores",
            output_bbox="boxes",
            threshold=args.threshold,
        )

    for image_path in args.images:
        image = Path(image_path)
        source = videoSource(str(image))
        frame = source.Capture()
        if frame is None:
            raise RuntimeError(f"Could not read image: {image}")

        detections = net.Detect(frame, overlay="none")
        print(f"\nImage: {image.name}")
        print(f"Detected objects: {len(detections)}")
        measurements = []
        for index, detection in enumerate(detections, start=1):
            class_name = (
                net.GetClassDesc(detection.ClassID)
                if labels is None
                else labels[detection.ClassID] if detection.ClassID < len(labels) else "UNKNOWN"
            )
            measurement = measure_detection(detection, class_name)
            measurements.append(measurement)
            print(f"  {index}. {describe_detection(measurement)}")

        output_path = output_dir / f"{image.stem}_detected{image.suffix}"
        output = videoOutput(str(output_path))
        output.Render(frame)
        del output
        draw_assignment_labels(output_path, measurements)
        print(f"Saved annotated image: {output_path}")


if __name__ == "__main__":
    main()

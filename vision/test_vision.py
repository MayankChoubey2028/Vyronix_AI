"""
Standalone test for the vision pipeline: Camera -> YOLO -> OCR -> SceneMemory

Run from your project root with:
    uv run python vision/test_vision.py

(Place this file inside your vision/ folder alongside camera.py, yolo_detector.py, ocr.py, scene_memory.py)
"""

import time

import cv2

from camera import Camera
from yolo_detector import ObjectDetector
from ocr import OCRReader
from scene_memory import SceneMemory


def main():
    print("=== Vision Pipeline Test ===\n")

    # 1. Camera
    print("[1/4] Opening camera...")
    t0 = time.time()
    cam = Camera()

    # Warm-up: let auto-exposure/auto-focus settle, and discard first few frames
    for _ in range(10):
        cam.get_frame()
        time.sleep(0.05)

    frame = cam.get_frame()
    t1 = time.time()

    if frame is None:
        print("FAILED: Could not capture frame.")
        cam.release()
        return

    print(f"OK - frame shape: {frame.shape} (took {t1 - t0:.2f}s)")

    # Save the frame so you can SEE exactly what was captured
    cv2.imwrite("captured_frame.jpg", frame)
    print("Saved captured frame to captured_frame.jpg - open it to check what the camera actually saw\n")

    # 2. YOLO detection
    print("[2/4] Running YOLO detection...")
    t0 = time.time()
    detector = ObjectDetector()
    objects = detector.detect(frame)
    t1 = time.time()
    print(f"OK - detected objects: {objects} (took {t1 - t0:.2f}s)\n")

    # 3. OCR
    print("[3/4] Running OCR...")
    t0 = time.time()
    ocr = OCRReader()
    text = ocr.extract_text(frame)
    t1 = time.time()
    print(f"OK - extracted text: '{text}' (took {t1 - t0:.2f}s)\n")

    # 4. Scene memory
    print("[4/4] Updating scene memory...")
    memory = SceneMemory()
    memory.update_objects(objects)
    memory.update_text(text)
    print(f"OK - scene state: {memory.get_scene()}\n")

    cam.release()
    print("=== All vision components passed ===")


if __name__ == "__main__":
    main()
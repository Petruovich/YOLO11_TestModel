from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="/YOLO_TEST_V1/data.yaml",
    epochs=1,
    imgsz=640,
    batch=16,
    name="yolo_test_run",
    workers=4
)

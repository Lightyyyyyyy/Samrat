import cv2
import torch
from ultralytics import YOLO

model = YOLO("yolov8x.pt")

video_path = r"C:\Users\Haseeb\OneDrive\Desktop\Samrat\Recording 2025-02-20 203718.mp4" #change the video path 
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    result = model(frame)

    for r in result:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])
            class_name = model.names[cls]

            if class_name in ["car", "truck", "bus", "motorcycle"]:
                color = (0, 255, 0)
                label = f"{class_name} {conf:.2f}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Traffic Video", frame)
    cv2.waitKey(1)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import torch
from ultralytics import YOLO
import csv


model = YOLO("yolov8m.pt")

video_paths = {
    "A": r"C:\Users\Haseeb\OneDrive\Desktop\Samrat\vcl.mp4",
    "B": r"C:\Users\Haseeb\OneDrive\Desktop\Samrat\vcl.mp4",
    "C": r"C:\Users\Haseeb\OneDrive\Desktop\Samrat\vcl.mp4",
    "D": r"C:\Users\Haseeb\OneDrive\Desktop\Samrat\vcl.mp4",
} #video feed for all 4 roads

caps = {road: cv2.VideoCapture(path) for road, path in video_paths.items()}


csv_file = open("vehicle_count_log.csv", "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Frame", "Road", "Total Vehicles"])


unique_vehicles = {road: set() for road in video_paths}

frame_number = 0

while all(cap.isOpened() for cap in caps.values()):
    frame_number += 1

    for road, cap in caps.items():
        ret, frame = cap.read()
        if not ret:
            continue

        result = model.track(frame, persist=True, tracker="bytetrack.yaml")  
        frame_vehicle_count = 0

        for r in result:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                class_name = model.names[cls]
                track_id = int(box.id[0]) if box.id is not None else None  

                if class_name in ["car", "truck", "bus", "motorcycle"] and track_id is not None:
                    if track_id not in unique_vehicles[road]:  
                        unique_vehicles[road].add(track_id)
                        frame_vehicle_count += 1

                    color = (0, 255, 0)
                    label = f"{class_name} {conf:.2f}"

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        count_text = f"Road {road} Vehicles: {len(unique_vehicles[road])}"
        cv2.putText(frame, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        
        csv_writer.writerow([frame_number, road, frame_vehicle_count])

        cv2.imshow(f"Traffic Video - Road {road}", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break


for cap in caps.values():
    cap.release()

cv2.destroyAllWindows()
csv_file.close()


for road, count in unique_vehicles.items():
    print(f"Total unique vehicles detected on Road {road}: {len(count)}")

print(f"\nOverall unique vehicles detected: {sum(len(v) for v in unique_vehicles.values())}")

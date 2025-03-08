import cv2
import csv
from ultralytics import YOLO


model = YOLO("yolov8m.pt")


video_path = r"C:\Users\Haseeb\OneDrive\Desktop\Samrat\vcl.mp4" #change to video feed
cap = cv2.VideoCapture(video_path)


csv_file = open("vehicle_count_log.csv", "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Frame", "Total Vehicles"])


unique_vehicles = set()
frame_number = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_number += 1
    result = model.track(frame, persist=True, tracker="bytetrack.yaml")  

    for r in result:
        for box in r.boxes:
            vehicle_id = int(box.id[0]) if box.id is not None else None  

            if vehicle_id is not None:
                unique_vehicles.add(vehicle_id) 

           
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])
            class_name = model.names[cls]
            color = (0, 255, 0)
            label = f"{class_name} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

  
    total_count = len(unique_vehicles)
    count_text = f"Total Vehicles: {total_count}"
    cv2.putText(frame, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    csv_writer.writerow([frame_number, total_count])

    cv2.imshow("Traffic Video", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
csv_file.close()
cv2.destroyAllWindows()

print(f"Total Unique Vehicles Detected: {len(unique_vehicles)}")

import cv2

video_path = r"C:\Users\Haseeb\OneDrive\Desktop\Samrat\Recording 2025-02-20 203718.mp4" #import the path of the video feed
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Traffic Video", frame)
    cv2.waitKey(1)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

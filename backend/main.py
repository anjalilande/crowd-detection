import cv2
from ultralytics import YOLO
import winsound

model = YOLO("yolov8n.pt")

camera = None
running = False

def generate_frames(mode, crowd_limit, video_path=None):

    global camera
    global running

    running = True

    # camera mode
    if mode == "camera":
        camera = cv2.VideoCapture(0)

    # video mode
    else:
        camera = cv2.VideoCapture(video_path)

    while running:

        success, frame = camera.read()

        if not success:
            break

        frame = cv2.resize(frame, (800, 500))

        results = model(frame, stream=True)

        people_count = 0
        status = "SAFE"
        box_color = (0,255,0)

        for r in results:

            for box in r.boxes:

                class_id = int(box.cls[0])

                if class_id == 0:

                    people_count += 1

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    if people_count > crowd_limit:

                        status = "DANGER"
                        box_color = (0,0,255)

                    else:

                        status = "SAFE"
                        box_color = (0,255,0)

                    cv2.rectangle(
                        frame,
                        (x1,y1),
                        (x2,y2),
                        box_color,
                        2
                    )

                    cv2.putText(
                        frame,
                        "P" + str(people_count),
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        box_color,
                        2
                    )

        # alert
        if people_count > crowd_limit:
            winsound.Beep(1000, 200)

        # top panel
        cv2.rectangle(frame, (10,10), (330,130), (0,0,0), -1)

        cv2.putText(
            frame,
            "Crowd Detection System",
            (20,35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,255),
            2
        )

        cv2.putText(
            frame,
            "People Count : " + str(people_count),
            (20,70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            "Status : " + status,
            (20,105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            box_color,
            2
        )

        # convert frame
        ret, buffer = cv2.imencode(".jpg", frame)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

    camera.release()

def stop_detection():

    global running

    running = False
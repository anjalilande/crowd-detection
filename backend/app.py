from flask import Flask, request, Response
from flask_cors import CORS
from main import generate_frames, stop_detection
import os

app = Flask(__name__)
CORS(app)

# store current settings
current_mode = "camera"
current_limit = 5
current_video = None

@app.route("/")
def home():

    return {
        "message":"Backend Running"
    }

# start detection
@app.route("/start-detection", methods=["POST"])
def start_detection():

    global current_mode
    global current_limit
    global current_video

    current_mode = request.form.get("mode")

    current_limit = int(request.form.get("crowd_limit"))

    video = request.files.get("video")

    current_video = None

    # save uploaded video
    if video:

        os.makedirs("uploads", exist_ok=True)

        current_video = os.path.join(
            "uploads",
            video.filename
        )

        video.save(current_video)

    return {
        "status":"Detection Started"
    }

# video stream route
@app.route("/video-feed")
def video_feed():

    return Response(

        generate_frames(
            current_mode,
            current_limit,
            current_video
        ),

        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# stop detection
@app.route("/stop-detection", methods=["POST"])
def stop():

    stop_detection()

    return {
        "status":"Detection Stopped"
    }

if __name__ == "__main__":
    app.run(debug=True)
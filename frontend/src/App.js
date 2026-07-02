import { useState } from "react";
import "./App.css";

function App() {

  const [mode, setMode] = useState("camera");
  const [crowdLimit, setCrowdLimit] = useState(5);
  const [videoFile, setVideoFile] = useState(null);

  const [streamStarted, setStreamStarted] = useState(false);
  const [status, setStatus] = useState("System Ready");

  // START DETECTION
  const startDetection = async () => {

    try {

      setStatus("Detection Running...");

      const formData = new FormData();

      formData.append("mode", mode);
      formData.append("crowd_limit", crowdLimit);

      // upload video if selected
      if(videoFile){
        formData.append("video", videoFile);
      }

      const response = await fetch(
        "http://127.0.0.1:5000/start-detection",
        {
          method:"POST",
          body:formData
        }
      );

      const data = await response.json();

      console.log(data);

      setStreamStarted(true);

    }

    catch(error){

      console.log(error);

      setStatus("Backend Connection Failed");

      alert("Backend Connection Failed");

    }

  };

  // STOP DETECTION
  const stopDetection = async () => {

    try {

      await fetch(
        "http://127.0.0.1:5000/stop-detection",
        {
          method:"POST"
        }
      );

      setStreamStarted(false);

      setStatus("System Stopped");

    }

    catch(error){

      console.log(error);

    }

  };

  return (

    <div className="container">

      <div className="dashboard">

        <h1>AI Crowd Detection System</h1>

        

        {/* STATUS BOX */}
        <div className="statusBox">

          <h3>System Status</h3>

          <p>{status}</p>

        </div>

        {/* SETTINGS */}
        <div className="settingsCard">

          <h2>Detection Settings</h2>

          <label>Select Detection Mode</label>

          <select
            value={mode}
            onChange={(e)=>setMode(e.target.value)}
          >

            <option value="camera">
              Live Camera
            </option>

            <option value="video">
              Upload Video
            </option>

          </select>

          {
            mode === "video" && (

              <div>

                <label>Upload Video</label>

                <input
                  type="file"
                  accept="video/*"
                  onChange={(e)=>setVideoFile(e.target.files[0])}
                />

              </div>
            )
          }

          <label>Set Crowd Limit</label>

          <input
            type="number"
            value={crowdLimit}
            onChange={(e)=>setCrowdLimit(e.target.value)}
          />

          <div className="buttonGroup">

            <button onClick={startDetection}>
              Start 
            </button>

            <button
              className="stopBtn"
              onClick={stopDetection}
            >
              Stop 
            </button>

          </div>

        </div>

        {/* VIDEO FEED */}
        {
          streamStarted && (

            <div className="videoSection">

              <h2 className="liveTitle">
                Detection Running...
              </h2>

              <div className="videoBox">

                <img
                  src="http://127.0.0.1:5000/video-feed"
                  alt="Video Feed"
                  className="videoFeed"
                />

              </div>

            </div>
          )
        }

      </div>

    </div>
  );
}

export default App;
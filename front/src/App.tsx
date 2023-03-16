// App.tsx

import { useRef, useState } from "react";

type Result = {
  name: string;
  confidence: string;
  top: number;
  right: number;
  bottom: number;
  left: number;
};

function App() {
  const [results, setResults] = useState<Result[]>([]);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const startCamera = async () => {
    if (videoRef.current) {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    }
  };

  const captureImage = async () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext("2d");
      if (context) {
        const width = videoRef.current.videoWidth;
        const height = videoRef.current.videoHeight;
        canvasRef.current.width = width;
        canvasRef.current.height = height;

        context.drawImage(videoRef.current, 0, 0, width, height);

        const imageData = context.getImageData(0, 0, width, height);
        context.putImageData(imageData, 0, 0);

        return new Promise<Blob>((resolve) => {
          canvasRef.current &&
            canvasRef.current.toBlob((blob) => {
              if (blob) {
                resolve(blob);
              }
            }, "image/jpeg");
        });
      }
    }
    return null;
  };

  const submitImage = async () => {
    const imageBlob = await captureImage();

    if (imageBlob) {
      const formData = new FormData();
      formData.append("image", imageBlob);

      const response = await fetch("http://127.0.0.1:8000/face_recognition", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setResults(data.results);
    }
  };
  console.log(results);
  return (
    <div>
      <h1>Face Recognition</h1>
      <button onClick={startCamera}>Start Camera</button>
      <button onClick={submitImage}>Submit Image</button>
      <video ref={videoRef} autoPlay></video>
      <canvas ref={canvasRef} style={{ display: "none" }}></canvas>
      <div>
        {results.map((result, index) => (
          <p key={index}>{result.name.slice(0, result.name.lastIndexOf("."))}</p>
        ))}
      </div>
    </div>
  );
}

export default App;

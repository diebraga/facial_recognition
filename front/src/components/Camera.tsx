// Camera.tsx
import React, { useRef, useEffect } from 'react';

const Camera: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    async function setupCamera() {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } else {
        console.error('Camera not available');
      }
    }

    setupCamera();
  }, []);

  return <video ref={videoRef} autoPlay />;
};

export default Camera;

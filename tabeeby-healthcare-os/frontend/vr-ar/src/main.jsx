import React from 'react';
import ReactDOM from 'react-dom/client';
import { Canvas } from '@react-three/fiber';
import { XR, XRButton } from '@react-three/xr';
import { OrbitControls, Environment } from '@react-three/drei';

function SurgicalScene() {
  return (
    <>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[2, 2, 2]} />
        <meshStandardMaterial color="#00bcd4" wireframe />
      </mesh>
      <mesh position={[3, 0, 0]}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial color="#ff5722" transparent opacity={0.5} />
      </mesh>
      <OrbitControls />
      <Environment preset="city" />
    </>
  );
}

function App() {
  return (
    <div style={{ width: '100vw', height: '100vh', background: '#0a0a0a' }}>
      <div style={{ position: 'absolute', top: 20, left: 20, zIndex: 10, color: 'white' }}>
        <h1>TABEEBY VR/AR</h1>
        <p>4D Surgical Interface - Metaverse OR</p>
        <XRButton mode="VR" />
      </div>
      <Canvas>
        <XR>
          <SurgicalScene />
        </XR>
      </Canvas>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);

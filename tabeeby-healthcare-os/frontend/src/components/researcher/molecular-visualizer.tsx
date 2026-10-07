import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export const MolecularVisualizer: React.FC<{ moleculeId: string }> = ({ moleculeId }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    if (!canvasRef.current) return;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: canvasRef.current });
    // TODO: Load molecular structure from PDB
  }, [moleculeId]);
  return <canvas ref={canvasRef} className="molecular-canvas" />;
};
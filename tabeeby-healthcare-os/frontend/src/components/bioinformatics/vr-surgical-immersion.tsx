import React, { useEffect, useRef } from 'react';

export const VRSurgicalImmersion: React.FC<{ procedureId: string }> = ({ procedureId }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    // VR surgical simulation loader
    if (!containerRef.current) return;
    const scene = document.createElement('div');
    scene.className = 'vr-scene';
    scene.innerHTML = '<h1>محاكاة الجراحة VR - الإجراء: ' + procedureId + '</h1>';
    containerRef.current.appendChild(scene);
  }, [procedureId]);
  return <div ref={containerRef} className="vr-container" />;
};
import React, { useEffect, useRef } from 'react';

export const MolecularSimulation: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    // Molecular dynamics simulation canvas
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let particles = [];
    for (let i = 0; i < 100; i++) {
      particles.push({
        x: Math.random() * canvas!.width,
        y: Math.random() * canvas!.height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        radius: Math.random() * 5 + 2
      });
    }
    const animate = () => {
      ctx!.clearRect(0, 0, canvas!.width, canvas!.height);
      particles.forEach(p => {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > canvas!.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas!.height) p.vy *= -1;
        ctx!.beginPath();
        ctx!.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx!.fillStyle = '#00d4ff';
        ctx!.fill();
      });
      requestAnimationFrame(animate);
    };
    animate();
  }, []);
  return <canvas ref={canvasRef} className="molecular-simulation" width="800" height="600" />;
};
import React, { useEffect, useRef, useState } from 'react';

export const MolecularSimulation = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [running, setRunning] = useState(true);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d')!;
    canvas.width = 600;
    canvas.height = 400;

    const particles = [];
    for (let i = 0; i < 50; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        r: Math.random() * 4 + 2,
        color: `hsl(${Math.random() * 360}, 70%, 60%)`
      });
    }

    const animate = () => {
      ctx.fillStyle = '#0a0a1a';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      particles.forEach(p => {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
      });
      if (running) requestAnimationFrame(animate);
    };
    animate();
  }, [running]);

  return (
    <div className="molecular-simulation">
      <h3>محاكاة جزيئية</h3>
      <canvas ref={canvasRef} className="mol-canvas" />
      <button onClick={() => setRunning(!running)}>
        {running ? 'إيقاف' : 'تشغيل'}
      </button>
    </div>
  );
};

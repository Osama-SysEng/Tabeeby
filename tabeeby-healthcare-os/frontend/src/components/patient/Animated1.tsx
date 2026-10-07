import React, { useEffect, useRef } from 'react';
// لوحة العلامات الحيوية المتحركة - بت updates كل 2 ثانية
export const AnimatedVitalsDashboard = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [vitals, setVitals] = React.useState({
    heartRate: 72,
    spo2: 98,
    bpSys: 120,
    bpDia: 80,
    temp: 37.0,
    glucose: 105,
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setVitals(prev => ({
        ...prev,
        heartRate: prev.heartRate + (Math.random() - 0.5) * 4,
        spo2: Math.max(95, Math.min(100, prev.spo2 + (Math.random() - 0.5) * 1)),
        bpSys: prev.bpSys + (Math.random() - 0.5) * 3,
        bpDia: prev.bpDia + (Math.random() - 0.5) * 2,
        temp: +(prev.temp + (Math.random() - 0.5) * 0.1).toFixed(1),
        glucose: +(prev.glucose + (Math.random() - 0.5) * 5).toFixed(0),
      }));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="animated-vitals-dashboard">
      <h3>العلامات الحيوية - تحديث فوري</h3>
      <div className="animated-vitals-grid">
        {Object.entries(vitals).map(([key, value]) => (
          <div key={key} className="animated-vital-card">
            <span className="vital-name">{key.replace(/([A-Z])/g, ' $1').trim()}</span>
            <span className="vital-value-pulse">{typeof value === 'number' ? value.toFixed(0) : value}</span>
            <span className="vital-unit">{key === 'glucose' ? 'mg/dL' : key === 'temp' ? '°C' : key === 'heartRate' ? 'bpm' : key === 'spo2' ? '%' : ''}</span>
          </div>
        ))}
      </div>
      <canvas ref={canvasRef} className="vitals-wave-canvas" />
    </div>
  );
};

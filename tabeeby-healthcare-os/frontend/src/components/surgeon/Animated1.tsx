import React, { useState, useEffect } from 'react';
// VR simulation animated
export const AnimatedVRSimulation = () => {
  const [procedures] = useState([
    { id: '1', name: 'استئصال الزائدة', duration: '45 min', steps: 24, currentStep: 0, running: false },
    { id: '2', name: 'CABG', duration: '4 ساعات', steps: 156, currentStep: 0, running: false },
  ]);
  const [selected, setSelected] = useState<typeof procedures[0] | null>(null);
  const [overallProgress, setOverallProgress] = useState(0);

  useEffect(() => {
    if (selected?.running) {
      const interval = setInterval(() => {
        setSelected(prev => {
          const nextStep = prev.currentStep + 1;
          if (nextStep >= prev.steps) {
            clearInterval(interval);
            return { ...prev, running: false, currentStep: prev.steps };
          }
          return { ...prev, currentStep: nextStep };
        });
        setOverallProgress(prev => Math.min(100, prev + 100 / (selected?.steps || 1)));
      }, 500);
      return () => clearInterval(interval);
    }
  }, [selected]);

  return (
    <div className="animated-vr-simulation">
      <h3>محاكاة الجراحة VR - 4D Experience</h3>
      <div className="vr-procedures-list">
        {procedures.map(p => (
          <div key={p.id} className={`vr-procedure-card ${selected?.id === p.id ? 'selected' : ''}`} onClick={() => setSelected({ ...p, running: true, currentStep: 0 })}>
            <div className="vr-procedure-header">
              <span className="vr-icon">🥽</span>
              <h4>{p.name}</h4>
            </div>
            <p>⏱ {p.duration} | {p.steps} خطوة</p>
            {selected?.id === p.id && (
              <div className="vr-progress-animated">
                <div className="vr-progress-bar"><div className="vr-progress-fill" style={{ width: ((selected.currentStep / selected.steps) * 100) + '%' }} /></div>
                <small>الخطوة {selected.currentStep} / {selected.steps}</small>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

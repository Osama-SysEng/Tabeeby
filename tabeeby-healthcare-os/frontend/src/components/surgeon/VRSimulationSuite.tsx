import React, { useState } from 'react';

const procedures = [
  { id: '1', name: 'استئصال الزائدة', duration: '45 min', complexity: 'متوسط' },
  { id: '2', name: 'CABG', duration: '4 ساعات', complexity: 'خبير' },
];

export const VRSimulationSuite = () => {
  const [selected, setSelected] = useState<typeof procedures[0] | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const start = () => { if (selected) setIsRunning(true); };
  return (
    <div className="vr-simulation">
      <h3>محاكاة الجراحة VR</h3>
      {procedures.map(p => (
        <div key={p.id} className={selected?.id === p.id ? 'selected' : ''}
          onClick={() => setSelected(p)}>
          <h4>{p.name}</h4>
          <p>⏱ {p.duration} | {p.complexity}</p>
        </div>
      ))}
      {selected && (
        <button onClick={start} disabled={isRunning}>
          {isRunning ? 'جاري...' : 'ابدأ المحاكاة'}
        </button>
      )}
    </div>
  );
};

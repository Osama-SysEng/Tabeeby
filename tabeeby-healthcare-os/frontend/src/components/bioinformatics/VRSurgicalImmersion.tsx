import React, { useState } from 'react';

const procedures = [
  { id: '1', name: 'استئصال الزائدة الدودية', duration: '45 min', complexity: 'متوسط' },
  { id: '2', name: 'زراعة الشريان التاجي', duration: '4 ساعات', complexity: 'خبير' },
];

export const VRSurgicalImmersion = () => {
  const [selected, setSelected] = useState<typeof procedures[0] | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  return (
    <div className="vr-surgical">
      <h3>غمر جراحي VR - 4D Simulation</h3>
      {procedures.map(p => (
        <div key={p.id} className={selected?.id === p.id ? 'selected' : ''}
          onClick={() => setSelected(p)}>
          <h4>{p.name}</h4>
          <p>⏱ {p.duration} | {p.complexity}</p>
        </div>
      ))}
      {selected && (
        <button onClick={() => setIsRunning(!isRunning)}>
          {isRunning ? 'إيقاف' : 'ابدأ المحاكاة'}
        </button>
      )}
      {isRunning && <p>بدء محاكاة: {selected.name}</p>}
    </div>
  );
};

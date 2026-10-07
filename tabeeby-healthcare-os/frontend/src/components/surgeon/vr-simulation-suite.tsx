import React, { useState } from 'react';

interface Procedure { id: string; name: string; duration: string; difficulty: string; haptics: boolean; }
export const VRSimulationSuite: React.FC = () => {
  const [procedures, setProcedures] = useState<Procedure[]>([
    { id: '1', name: 'Appendectomy', duration: '45 min', difficulty: 'Intermediate', haptics: true },
    { id: '2', name: 'CABG', duration: '4 hours', difficulty: 'Expert', haptics: true },
    { id: '3', name: 'Laparoscopic Cholecystectomy', duration: '60 min', difficulty: 'Intermediate', haptics: true },
  ]);
  const [selected, setSelected] = useState<Procedure | null>(null);
  const startSimulation = () => { if (selected) alert(`Starting VR simulation: ${selected.name}`); };
  return (
    <div className="vr-simulation-suite">
      <h2>محاكاة الجراحة VR</h2>
      <div className="procedure-list">
        {procedures.map(p => (
          <div key={p.id} className="procedure-card" onClick={() => setSelected(p)}>
            <h3>{p.name}</h3>
            <p>المدة: {p.duration} | الصعوبة: {p.difficulty}</p>
            <p>الارتجاج: {p.haptics ? 'مفعّل' : 'غير مفعل'}</p>
          </div>
        ))}
      </div>
      {selected && (
        <div className="simulation-controls">
          <h3>بدأ المحاكاة: {selected.name}</h3>
          <button onClick={startSimulation}>ابدأ المحاكاة</button>
          <button disabled>إيقاف</button>
        </div>
      )}
    </div>
  );
};
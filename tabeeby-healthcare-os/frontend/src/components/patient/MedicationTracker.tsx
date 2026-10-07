import React, { useState } from 'react';
import { Pill, Check, X } from '../icons';

const initialMeds = [
  { id: '1', name: 'أدوية الضغط', dosage: '10mg', time: '08:00', taken: false },
  { id: '2', name: 'أدوية السكر', dosage: '5mg', time: '08:00', taken: false },
];

export const MedicationTracker = () => {
  const [meds, setMeds] = useState(initialMeds);
  const toggle = (id: string) => setMeds(meds.map(m => m.id === id ? { ...m, taken: !m.taken } : m));
  return (
    <div className="medication-tracker">
      <h3>المواعيد الدوائية</h3>
      {meds.map(m => (
        <div key={m.id} className={m.taken ? 'taken' : 'pending'}>
          <Pill />
          <span>{m.name} - {m.dosage} - {m.time}</span>
          <button onClick={() => toggle(m.id)}>
            {m.taken ? <Check /> : <X />}
          </button>
        </div>
      ))}
    </div>
  );
};

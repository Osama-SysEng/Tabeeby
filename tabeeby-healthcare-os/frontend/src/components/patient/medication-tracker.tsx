import React, { useState } from 'react';
import { Pill, Check, Alert } from '../icons';

interface Medication { name: string; dosage: string; time: string; taken: boolean; }
export const MedicationTracker: React.FC = () => {
  const [meds, setMeds] = useState<Medication[]>([]);
  const markTaken = (idx: number) => {
    setMeds(meds.map((m, i) => i === idx ? { ...m, taken: true } : m));
  };
  return (
    <div className="medication-tracker">
      <h2>المواعيد الدوائية</h2>
      {meds.map((m, i) => (
        <div key={i} className={`med-card ${m.taken ? 'taken' : 'pending'}`}>
          <Pill /><span>{m.name}</span><span>{m.dosage}</span>
          <button onClick={() => markTaken(i)}>{m.taken ? 'تم' : 'تناول'}</button>
        </div>
      ))}
    </div>
  );
};
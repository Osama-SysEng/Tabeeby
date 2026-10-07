import React, { useState } from 'react';

export const SymptomChecker: React.FC = () => {
  const [symptoms, setSymptoms] = useState<string[]>([]);
  const [result, setResult] = useState<any>(null);
  const checkSymptoms = async () => {
    const res = await fetch('/api/diagnostic/symptom-check', {
      method: 'POST',
      body: JSON.stringify({ symptoms })
    });
    setResult(await res.json());
  };
  return (
    <div className="symptom-checker">
      <h2>فحص الأعراض</h2>
      <input placeholder="أضف عرض..." onKeyDown={e => { if(e.key==='Enter') setSymptoms([...symptoms, e.target.value]); }} />
      <button onClick={checkSymptoms}>فحص</button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
};
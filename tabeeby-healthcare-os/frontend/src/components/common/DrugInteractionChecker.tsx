import React, { useState } from 'react';
export const DrugInteractionChecker = () => {
  const [d1, setD1] = useState(''); const [d2, setD2] = useState(''); const [result, setResult] = useState<any>(null);
  const check = async () => {
    const r = await fetch('/api/physician/drug-interaction', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ drug1: d1, drug2: d2 }) });
    setResult(await r.json());
  };
  return (
    <div className="drug-checker">
      <h3>فحص تفاعلات الأدوية</h3>
      <input value={d1} onChange={e => setD1(e.target.value)} placeholder="دواء 1" />
      <input value={d2} onChange={e => setD2(e.target.value)} placeholder="دواء 2" />
      <button onClick={check}>فحص</button>
      {result && <div className="interaction-result"></div>}
    </div>
  );
};

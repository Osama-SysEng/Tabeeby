import React, { useState } from 'react';

export const DrugInteractionChecker = () => {
  const [drug1, setDrug1] = useState('');
  const [drug2, setDrug2] = useState('');
  const [interaction, setInteraction] = useState<any>(null);
  const check = async () => {
    const res = await fetch('/api/physician/drug-interaction', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ drug1, drug2 })
    });
    setInteraction(await res.json());
  };
  return (
    <div className="drug-checker">
      <h3>فحص تفاعلات الأدوية</h3>
      <input value={drug1} onChange={e => setDrug1(e.target.value)} placeholder="دواء 1" />
      <input value={drug2} onChange={e => setDrug2(e.target.value)} placeholder="دواء 2" />
      <button onClick={check}>فحص</button>
      {interaction && <div className="interaction-result">{interaction.level}: {interaction.message}</div>}
    </div>
  );
};

import React, { useState } from 'react';

export const DrugInteractionChecker: React.FC = () => {
  const [drug1, setDrug1] = useState('');
  const [drug2, setDrug2] = useState('');
  const [interaction, setInteraction] = useState<any>(null);
  
  const checkInteraction = async () => {
    const res = await fetch('/api/physician/drug-interaction', {
      method: 'POST',
      body: JSON.stringify({ drug1, drug2 })
    });
    setInteraction(await res.json());
  };
  return (
    <div className="drug-interaction-checker">
      <h2>فحص تفاعلات الأدوية</h2>
      <input value={drug1} onChange={e => setDrug1(e.target.value)} placeholder="دواء 1" />
      <input value={drug2} onChange={e => setDrug2(e.target.value)} placeholder="دواء 2" />
      <button onClick={checkInteraction}>فحص</button>
      {interaction && <pre>{JSON.stringify(interaction, null, 2)}</pre>}
    </div>
  );
};
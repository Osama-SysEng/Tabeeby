import React, { useState } from 'react';

export const SymptomChecker = () => {
  const [symptoms, setSymptoms] = useState<string[]>([]);
  const [query, setQuery] = useState('');
  const [result, setResult] = useState<any>(null);

  const add = () => {
    if (query.trim()) {
      setSymptoms([...symptoms, query.trim()]);
      setQuery('');
    }
  };

  const check = async () => {
    const res = await fetch('/api/diagnostic/symptom-check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symptoms })
    });
    setResult(await res.json());
  };

  return (
    <div className="symptom-checker">
      <h3>فحص الأعراض</h3>
      <input value={query} onChange={e => setQuery(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && add()}
        placeholder="أضف عرضاً..." />
      <button onClick={add}>إضافة</button>
      <div className="symptom-tags">
        {symptoms.map((s, i) => (
          <span key={i} className="symptom-tag">{s} ✕</span>
        ))}
      </div>
      <button className="check-btn" onClick={check}>تحليل</button>
      {result && <div className="symptom-result">{result.possibleConditions}</div>}
    </div>
  );
};

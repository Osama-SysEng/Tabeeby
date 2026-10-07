import React, { useState } from 'react';

interface TreatmentOption { id: string; name: string; efficacy: number; evidence: string; sideEffects: string[]; }
interface TreatmentRecommenderProps { physicianId: string; patientId?: string; }

export const TreatmentRecommender: React.FC<TreatmentRecommenderProps> = ({ physicianId, patientId }) => {
  const [treatments, setTreatments] = useState<TreatmentOption[]>([]);
  const [patientIdState, setPatientIdState] = useState(patientId || '');
  
  const fetchRecommendations = async () => {
    const res = await fetch(`/api/physician/${physicianId}/recommend`, {
      method: 'POST',
      body: JSON.stringify({ patientId: patientIdState })
    });
    setTreatments(await res.json());
  };
  return (
    <div className="treatment-recommender">
      <h2>التوصيات العلاجية - Ultra IQ</h2>
      <input value={patientIdState} onChange={e => setPatientIdState(e.target.value)} placeholder="م troop المريض" />
      <button onClick={fetchRecommendations}>جلب التوصيات</button>
      {treatments.map(t => (
        <div key={t.id} className="treatment-card">
          <h3>{t.name}</h3>
          <p>الفعالية: {t.efficacy}%</p>
          <p>الأدلة: {t.evidence}</p>
          <ul>{t.sideEffects.map(se => <li key={se}>{se}</li>)}</ul>
        </div>
      ))}
    </div>
  );
};
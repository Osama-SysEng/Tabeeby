import React, { useState } from 'react';

interface Trial { id: string; title: string; phase: string; condition: string; location: string; eligibility: string; }
export const ClinicalTrialMatcher: React.FC<{ patientId: string }> = ({ patientId }) => {
  const [trials, setTrials] = useState<Trial[]>([]);
  const matchTrials = async () => {
    const res = await fetch(`/api/physician/${patientId}/trials`);
    setTrials(await res.json());
  };
  return (
    <div className="clinical-trial-matcher">
      <h2>التجارب السريرية المتطابقة</h2>
      <button onClick={matchTrials}>جلب التجارب</button>
      {trials.map(t => (
        <div key={t.id} className="trial-card">
          <h3>{t.title}</h3>
          <p>المرحلة: {t.phase}</p>
          <p>الحالة: {t.condition}</p>
          <p>الموقع: {t.location}</p>
        </div>
      ))}
    </div>
  );
};
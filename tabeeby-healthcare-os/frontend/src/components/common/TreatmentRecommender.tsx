import React from 'react';
const treatments = [
  { name: 'دواء الأTEENسين', efficacy: 87, evidence: 'NEJM 2024', sideEffects: ['صداع', 'جفاف الفم'] },
  { name: 'العلاج الفيزيائي', efficacy: 76, evidence: 'Lancet 2023', sideEffects: ['تعب مؤقت'] },
];
export const TreatmentRecommender = () => (
  <div className="treatment-recommender">
    <h3>توصيات العلاج -Ultra IQ</h3>
    {treatments.map(t => (
      <div key={t.name} className="treatment-card">
        <h4>{t.name}</h4>
        <p>الفعالية: {t.efficacy}% | الدليل: {t.evidence}</p>
        <ul>{t.sideEffects.map(s => <li key={s}>{s}</li>)}</ul>
        <button>إضافة للعلاج</button>
      </div>
    ))}
  </div>
);

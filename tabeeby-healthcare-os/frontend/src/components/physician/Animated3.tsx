import React, { useState } from 'react';
// توصيات العلاج مع cards متحركة
export const AnimatedTreatmentRecommender = () => {
  const [treatments] = useState([
    { id: '1', name: 'دواء الأTEENسين', efficacy: 87, evidence: 'NEJM 2024', sideEffects: ['صداع خفيف', 'جفاف الفم'], color: '#4CAF50' },
    { id: '2', name: 'العلاج الفيزيائي', efficacy: 76, evidence: 'Lancet 2023', sideEffects: ['تعب مؤقت'], color: '#2196F3' },
    { id: '3', name: 'العلاج الدوائي البديل', efficacy: 68, evidence: 'JAMA 2025', sideEffects: ['غثيان', 'دوار'], color: '#FF9800' },
  ]);
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div className="animated-treatment-recommender">
      <h3>توصيات العلاج -Ultra IQ (مصنّف حسب الأدلة)</h3>
      <div className="treatment-cards-container">
        {treatments.map(t => (
          <div key={t.id} className={`treatment-card ${selected === t.id ? 'selected' : ''}`} onClick={() => setSelected(t.id)} style={{ borderColor: t.color }}>
            <div className="treatment-header">
              <h4>{t.name}</h4>
              <span className="efficacy-badge" style={{ backgroundColor: t.color }}>{t.efficacy}%</span>
            </div>
            <p className="treatment-evidence">{t.evidence}</p>
            <ul className="side-effects-list">
              {t.sideEffects.map(s => <li key={s}>{s}</li>)}
            </ul>
            <button className="add-treatment-btn">إضافة للعلاج</button>
          </div>
        ))}
      </div>
    </div>
  );
};

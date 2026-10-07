import React from 'react';

const risks = [
  { region: 'القاهرة', condition: 'السكري', risk: 'high', percent: 18.4 },
  { region: 'الإسكندرية', condition: 'ارتفاع ضغط الدم', risk: 'medium', percent: 22.1 },
];

export const PopulationGenetics = () => (
  <div className="population-genetics">
    <h3>التStratification الوراثي</h3>
    {risks.map(r => (
      <div key={r.region} className={r.risk}>
        <h4>{r.region}</h4>
        <p>{r.condition} - خطر: {r.risk} - {r.percent}%</p>
      </div>
    ))}
  </div>
);

import React, { useState } from 'react';

interface GeneticRisk { region: string; condition: string; riskLevel: string; populationPercent: number; }
export const PopulationGenetics: React.FC = () => {
  const [risks, setRisks] = useState<GeneticRisk[]>([]);
  return (
    <div className="population-genetics">
      <h2>التStratification الوراثي للسكان</h2>
      {risks.map(r => (
        <div key={r.region + r.condition} className="genetic-risk">
          <h3>{r.region} - {r.condition}</h3>
          <p>الخطر: {r.riskLevel}</p>
          <p>النسبة: {r.populationPercent}%</p>
        </div>
      ))}
    </div>
  );
};
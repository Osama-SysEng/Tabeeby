import React, { useEffect, useState } from 'react';

interface RegionData { region: string; cases: number; trend: string; riskLevel: string; }
export const EpidemicMap: React.FC = () => {
  const [regions, setRegions] = useState<RegionData[]>([]);
  useEffect(() => {
    fetch('/api/national/epidemic-data').then(r => r.json()).then(setRegions);
  }, []);
  return (
    <div className="epidemic-map">
      <h2>رصد الأوبئة - Ultra IQ (تنبيه مبكر)</h2>
      {regions.map(r => (
        <div key={r.region} className={`region-card ${r.riskLevel}`}>
          <h3>{r.region}</h3>
          <p>الCases: {r.cases}</p>
          <p>الاتجاه: {r.trend}</p>
          <p>مستوى الخطر: {r.riskLevel}</p>
        </div>
      ))}
    </div>
  );
};
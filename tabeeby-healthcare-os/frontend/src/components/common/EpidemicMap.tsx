import React from 'react';
const regions = [
  { name: 'القاهرة', cases: 1245, trend: 'up', risk: 'high' },
  { name: 'الإسكندرية', cases: 876, trend: 'stable', risk: 'medium' },
  { name: 'أسيوط', cases: 342, trend: 'down', risk: 'low' },
];
export const EpidemicMap = () => (
  <div className="epidemic-map">
    <h3>رصد الأوبئة - تنبيه مبكر Ultra IQ</h3>
    {regions.map(r => (
      <div key={r.name} className={r.risk}>
        <h4>{r.name}</h4>
        <p>{r.cases} حالة | {r.trend === 'up' ? '↑' : r.trend === 'down' ? '↓' : '→'}</p>
      </div>
    ))}
  </div>
);

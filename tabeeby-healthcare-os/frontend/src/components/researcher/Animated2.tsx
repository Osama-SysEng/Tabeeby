import React, { useEffect, useState } from 'react';
// خريطة الأوبئة متحركة مع markers تتحرك
export const AnimatedEpidemicMap = () => {
  const [regions, setRegions] = useState([
    { id: '1', name: 'القاهرة', cases: 1245, trend: 'up', risk: 'high', pulse: 0 },
    { id: '2', name: 'الإسكندرية', cases: 876, trend: 'stable', risk: 'medium', pulse: 0 },
    { id: '3', name: 'أسيوط', cases: 342, trend: 'down', risk: 'low', pulse: 0 },
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setRegions(prev => prev.map(r => ({
        ...r,
        pulse: (r.pulse + 1) % 100,
        cases: r.trend === 'up' ? r.cases + Math.floor(Math.random() * 5) : r.trend === 'down' ? r.cases - Math.floor(Math.random() * 3) : r.cases,
      }));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="animated-epidemic-map">
      <h3>رصد الأوبئة - تنبيه مبكر Ultra IQ</h3>
      <div className="animated-map-regions">
        {regions.map(r => (
          <div key={r.id} className={`animated-region ${r.risk}`} style={{ '--pulse': r.pulse + '%' }}>
            <div className="region-pulse" />
            <h4>{r.name}</h4>
            <p className="cases-value">{r.cases} حالة</p>
            <span className={`trend-indicator ${r.trend}`}>
              {r.trend === 'up' ? '↑ متزايد' : r.trend === 'down' ? '↓ متناقص' : '→ مستقر'}
            </span>
            <span className="risk-badge">مستوى الخطر: {r.risk}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

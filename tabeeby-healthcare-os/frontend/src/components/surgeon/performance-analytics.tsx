import React, { useEffect, useState } from 'react';

interface Metric { name: string; value: number; target: number; trend: string; }
export const PerformanceAnalytics: React.FC<{ surgeonId: string }> = ({ surgeonId }) => {
  const [metrics, setMetrics] = useState<Metric[]>([]);
  useEffect(() => {
    fetch(`/api/surgical/${surgeonId}/performance`).then(r => r.json()).then(setMetrics);
  }, [surgeonId]);
  return (
    <div className="performance-analytics">
      <h2>تحليلات الأداء - الجراح {surgeonId}</h2>
      {metrics.map(m => (
        <div key={m.name} className="metric-card">
          <h3>{m.name}</h3>
          <p>الحالي: {m.value} | الهدف: {m.target}</p>
          <span className={m.trend === 'up' ? 'trend-up' : 'trend-down'}>{m.trend}</span>
        </div>
      ))}
    </div>
  );
};
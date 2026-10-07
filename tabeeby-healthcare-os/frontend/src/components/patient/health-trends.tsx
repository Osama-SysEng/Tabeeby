import React, { useEffect, useState } from 'react';

interface HealthTrend { date: string; value: number; metric: string; }
interface HealthTrendsProps { patientId: string; }

export const HealthTrends: React.FC<HealthTrendsProps> = ({ patientId }) => {
  const [trends, setTrends] = useState<HealthTrend[]>([]);
  useEffect(() => {
    fetch(`/api/patient/${patientId}/trends?period=30d`).then(r => r.json()).then(setTrends);
  }, [patientId]);
  return (
    <div className="health-trends">
      <h2>الاتجاهات الصحية (30 يوم)</h2>
      {trends.map(t => <div key={t.date} className="trend-item">{t.metric}: {t.value}</div>)}
    </div>
  );
};
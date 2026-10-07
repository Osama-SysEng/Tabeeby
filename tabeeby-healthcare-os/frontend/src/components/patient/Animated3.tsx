import React, { useEffect, useState } from 'react';
// لوحة التأثير الصحي مع رسوم متحركة - الطقس + الصحة
export const AnimatedHealthDashboard = () => {
  const [weather, setWeather] = useState<any>(null);
  const [trends, setTrends] = useState([
    { metric: 'النبض', value: 72, target: 65, unit: 'bpm', trend: 'down' },
    { metric: 'ضغط الدم', value: '120/80', target: '115/75', trend: 'down' },
    { metric: 'السكر', value: '105', target: '95', trend: 'down', unit: 'mg/dL' },
  ]);
  const [step, setStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStep(prev => (prev + 1) % trends.length);
      setTrends(prev => prev.map((t, i) =>
        i === prev ? { ...t, value: t.value + (Math.random() - 0.5) * (t.unit === 'mg/dL' ? 5 : t.unit === 'bpm' ? 3 : 5) } : t
      ));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="animated-health-dashboard">
      <h3>لوحة الصحة المتكاملة - بيانات حية</h3>
      <div className="health-metrics">
        {trends.map((t, i) => (
          <div key={i} className={`health-metric ${step === i ? 'highlighted' : ''}`}>
            <div className="metric-header">
              <span>{t.metric}</span>
              <span className="trend-arrow">{t.trend === 'down' ? '📉' : '📈'}</span>
            </div>
            <div className="metric-value">{t.value} <small>{t.unit}</small></div>
            <div className="metric-target">الهدف: {t.target}</div>
            <div className="metric-bar"><div className="metric-fill" style={{ width: Math.min(100, (t.value / (parseInt(String(t.target).toString()) || 100)) * 100) + '%' }} /></div>
          </div>
        ))}
      </div>
      <div className="weather-card">
        <h4>الطقس وتأثيره على الصحة</h4>
        {weather && <p>الحرارة: {weather.temp}°C | الرطوبة: {weather.humidity}%</p>}
        {!weather && <p>جاري تحميل البيانات...</p>}
      </div>
    </div>
  );
};

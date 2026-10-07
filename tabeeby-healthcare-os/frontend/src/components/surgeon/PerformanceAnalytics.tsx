import React from 'react';

const metrics = [
  { name: 'دقة القطع', value: 94, target: 95 },
  { name: 'وقت الإجراء', value: 38, target: 45 },
  { name: 'معدل المضاعفات', value: 2.1, target: 3.0 },
  { name: 'راحة المريض', value: 88, target: 90 },
];

export const PerformanceAnalytics = () => {
  const overall = metrics.reduce((s, m) => s + m.value, 0) / metrics.length;
  return (
    <div className="performance-analytics">
      <h3>تحليلات الأداء</h3>
      <div className="overall-score">
        <h2>النتيجة الإجمالية: {overall.toFixed(1)}%</h2>
        <div className="score-bar"><div style={{ width: overall + '%' }} /></div>
      </div>
      {metrics.map(m => (
        <div key={m.name} className="metric-card">
          <h4>{m.name}</h4>
          <p>{m.value}% (الهدف: {m.target}%)</p>
        </div>
      ))}
    </div>
  );
};

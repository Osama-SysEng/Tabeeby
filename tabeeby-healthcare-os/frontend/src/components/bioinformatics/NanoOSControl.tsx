import React from 'react';

const missions = [
  { id: '1', target: 'ورم الكبد - اليسار', payload: 'doxorubicin', status: 'active', progress: 67 },
  { id: '2', target: 'العلاج المناعي', payload: 'anti-PD1', status: 'navigating', progress: 23 },
];

export const NanoOSControl = () => (
  <div className="nano-os-control">
    <h3>نظام النانو التشغيلي - Nano-OS</h3>
    {missions.map(m => (
      <div key={m.id} className={m.status}>
        <h4>{m.target}</h4>
        <div className="progress-bar"><div style={{ width: m.progress + '%' }} /></div>
        <span>{m.progress}% | payload: {m.payload}</span>
      </div>
    ))}
  </div>
);

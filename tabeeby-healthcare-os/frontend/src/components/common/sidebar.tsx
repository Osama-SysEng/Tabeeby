import React from 'react';
const nav: Record<number, string[]> = {
  1: ['Dashboard', 'Vitals', 'AI Doctor', 'Medications', 'Appointments'],
  2: ['Patients', 'Alerts', 'Labs', 'Imaging', 'Treatment'],
  3: ['Drug Pipeline', 'Epidemic Map', 'Genetics', 'Literature'],
  4: ['Bio-Robot', 'Nano-OS', 'Simulation', 'VR'],
  5: ['VR Suite', 'AR Assist', 'Metaverse OR', 'Robotic Control'],
};
export const Sidebar = ({ tier, userName }: { tier: number; userName: string }) => (
  <nav className="sidebar">
    <div className="sidebar-header"><span>👤 {userName}</span><span className="tier-label">Tier {tier}</span></div>
    {nav[tier]?.map(item => <div key={item} className="nav-item">📌 {item}</div>)}
  </nav>
);

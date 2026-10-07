import React from 'react';
import { Heart } from '../icons';

interface VitalSign { label: string; value: string; unit: string; status: 'normal' | 'warning' | 'critical'; }
interface VitalsPanelProps { vitals: VitalSign[] | null; }

export const VitalMonitor: React.FC<VitalsPanelProps> = ({ vitals }) => {
  if (!vitals) return <div className="vitals-loading">جاري التحميل...</div>;
  return (
    <div className="vitals-grid">
      {vitals.map(v => (
        <div key={v.label} className={`vital-card ${v.status}`}>
          <Heart />
          <span>{v.label}: {v.value} {v.unit}</span>
          <small>{v.status}</small>
        </div>
      ))}
    </div>
  );
};"
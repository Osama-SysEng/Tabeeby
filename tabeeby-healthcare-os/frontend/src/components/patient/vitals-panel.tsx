import React from 'react';
import { HeartRate, Oxygen, BloodPressure, Temperature, Glucose } from '../icons';

interface VitalSign { label: string; value: string; unit: string; status: 'normal' | 'warning' | 'critical'; }
interface VitalsPanelProps { vitals: VitalSign[] | null; }

export const VitalsPanel: React.FC<VitalsPanelProps> = ({ vitals }) => {
  if (!vitals) return <div className="vitals-loading">جاري تحميل العلامات الحيوية...</div>;
  return (
    <div className="vitals-panel">
      <h2>العلامات الحيوية الحالية</h2>
      {vitals.map(v => (
        <div key={v.label} className={`vital-card ${v.status}`}>
          <h3>{v.label}</h3>
          <span className="value">{v.value}</span>
          <span className="unit">{v.unit}</span>
          <span className={`status ${v.status}`}>{v.status}</span>
        </div>
      ))}
    </div>
  );
};
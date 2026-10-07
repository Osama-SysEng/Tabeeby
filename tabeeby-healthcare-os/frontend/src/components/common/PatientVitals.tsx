import React from 'react';
import { Heart, Oxygen, BloodPressure, Temperature, Glucose, AlertTriangle } from '../icons';
const sampleVitals = [
  { label: 'النبض', value: '72', unit: 'bpm', status: 'normal' },
  { label: 'SpO2', value: '98', unit: '%', status: 'normal' },
  { label: 'ضغط الدم', value: '120/80', unit: '', status: 'normal' },
  { label: 'السكر', value: '105', unit: 'mg/dL', status: 'warning' },
];
export const PatientVitals = () => (
  <div className="vital-monitor">
    <h3>العلامات الحيوية - Ultra IQ Monitoring</h3>
    <div className="vital-grid">
      {sampleVitals.map(v => (
        <div key={v.label} className={`vital-card ${v.status}`}>
          {v.status === 'critical' && <AlertTriangle />}
          <span className="vital-label">{v.label}</span>
          <span className="vital-value">{v.value}</span>
          <span className="vital-unit">{v.unit}</span>
          <span className={`vital-status ${v.status}`}>{v.status}</span>
        </div>
      ))}
    </div>
  </div>
);

import React from 'react';
import { User, Heart, Alert } from '../icons';

interface Patient { id: string; name: string; age: number; status: string; vitals: any; alerts: any[]; }

export const PatientCard: React.FC<{ patient: Patient }> = ({ patient }) => {
  const hasCritical = patient.alerts.some(a => a.level === 'critical');
  return (
    <div className={`patient-card ${hasCritical ? 'critical' : ''}`}>
      <User />
      <h3>{patient.name}</h3>
      <p>العمر: {patient.age}</p>
      <div className="vitals-mini">
        {patient.vitals && Object.entries(patient.vitals).map(([k, v]) => (
          <span key={k}>{k}: {v}</span>
        ))}
      </div>
      {hasCritical && <Alert className="critical-alert" />}
      <button className="view-btn">عرض التفاصيل</button>
    </div>
  );
};
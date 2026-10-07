import React from 'react';
import { User, Alert } from '../icons';

interface Patient { id: string; name: string; age: number; status: string; alerts: string[]; }
export const DoctorPatientList = ({ patients }: { patients: Patient[] }) => (
  <div className="patient-grid">
    {patients.slice(0, 50).map(p => (
      <div key={p.id} className={p.alerts.length > 0 ? 'has-alert' : ''}>
        <User />
        <h3>{p.name} - {p.age} سنة</h3>
        <p>الحالة: {p.status}</p>
        {p.alerts.length > 0 && (
          <Alert />
          <p>{p.alerts[0]}</p>
        )}
        <button>عرض السجل</button>
      </div>
    ))}
  </div>
);

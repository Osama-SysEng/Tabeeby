import React from 'react';
import { Bell } from '../icons';

interface Alert { id: string; type: string; message: string; predictedTime: string; confidence: number; patientId: string; }

export const UltraIQAlert: React.FC<{ alerts: Alert[] }> = ({ alerts }) => {
  return (
    <div className="ultra-iq-alerts">
      <h2>تنبيهات Ultra IQ</h2>
      {alerts.map(a => (
        <div key={a.id} className="iq-alert">
          <strong>{a.type}</strong>
          <p>{a.message}</p>
          <span className="predicted">الوقت المتوقع: {a.predictedTime}</span>
          <span className="confidence">الثقة: {a.confidence}%</span>
          <button onClick={() => window.location.href = `/physician/patient/${a.patientId}`}>عرض</button>
        </div>
      ))}
    </div>
  );
};
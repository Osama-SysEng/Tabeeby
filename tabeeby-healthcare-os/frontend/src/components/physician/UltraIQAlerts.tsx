import React from 'react';
import { Bell } from '../icons';

interface Alert { id: string; message: string; secondsBefore: number; confidence: number; }
export const UltraIQAlerts = ({ physicianId }: { physicianId: string }) => {
  const [alerts, setAlerts] = useState<Alert[]>([
    { id: '1', message: 'انخفاض نبض المريض #1234 - قد يشير إلى arrhythmia', secondsBefore: 45, confidence: 92 },
  ]);
  const acknowledge = (id: string) => setAlerts(prev => prev.filter(a => a.id !== id));
  return (
    <div className="ultra-iq-alerts">
      <h3>تنبيهات Ultra IQ - 30-120 ثانية قبل الحدث</h3>
      {alerts.map(a => (
        <div key={a.id} className="alert-item">
          <Bell />
          <strong>{a.message}</strong>
          <span>⏰ قبل {a.secondsBefore} ثانية | 🎯 ثقة {a.confidence}%</span>
          <button onClick={() => acknowledge(a.id)}>تم الاعتراف</button>
        </div>
      ))}
    </div>
  );
};

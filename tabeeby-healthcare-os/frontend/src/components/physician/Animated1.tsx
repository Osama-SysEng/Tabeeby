import React, { useState, useEffect } from 'react';
// لوحة الطبيب مع مريض cards تتحرك وتنبض
export const AnimatedPatientGrid = () => {
  const [patients] = useState([
    { id: '1', name: 'أحمد محمد', age: 45, heartRate: 88, bp: '140/90', status: 'monitoring', alert: false },
    { id: '2', name: 'فاطمة أحمد', age: 52, heartRate: 72, bp: '115/75', status: 'stable', alert: false },
    { id: '3', name: 'يوسف عمر', age: 38, heartRate: 105, bp: '155/100', status: 'critical', alert: true },
    { id: '4', name: 'سارة عبد الله', age: 67, heartRate: 68, bp: '125/80', status: 'stable', alert: false },
    { id: '5', name: 'خالد صالح', age: 41, heartRate: 92, bp: '135/88', status: 'warning', alert: true },
  ]);

  return (
    <div className="animated-patient-grid">
      <h3>مرضى النشط - 50 مريض (Ultra IQ Dashboard)</h3>
      <div className="patient-cards-grid">
        {patients.map((p, i) => (
          <div key={p.id} className={`patient-card-animated ${p.alert ? 'alert-card' : ''} ${p.status}`} style={{ animationDelay: `${i * 0.1}s` }}>
            <div className="patient-card-header">
              <span className="patient-avatar">{p.name.charAt(0)}</span>
              <h4>{p.name}</h4>
              <span className="patient-age">{p.age} سنة</span>
            </div>
            <div className="patient-vitals">
              <div className="vital-item"><span>❤️</span> {p.heartRate} bpm</div>
              <div className="vital-item"><span>🩸</span> {p.bp}</div>
            </div>
            <div className="patient-status-badge">{p.status}</div>
            {p.alert && <div className="alert-badge">🔔 تنبيه</div>}
          </div>
        ))}
      </div>
    </div>
  );
};

import React from 'react';
// PatientVitals with pulse animation
export const AnimatedPatientVitals = () => {
  const [vitals] = React.useState([
    { label: 'النبض', value: 72, unit: 'bpm', icon: '❤️', status: 'normal' },
    { label: 'SpO2', value: 98, unit: '%', icon: '🫁', status: 'normal' },
    { label: 'ضغط الدم', value: '120/80', unit: '', icon: '🩸', status: 'normal' },
    { label: 'السكر', value: 105, unit: 'mg/dL', icon: '🍬', status: 'warning' },
  ]);
  return (
    <div className="animated-vitals">
      <h3>العلامات الحيوية - Ultra IQ</h3>
      <div className="animated-vital-grid">
        {vitals.map((v, i) => (
          <div key={v.label} className={`animated-vital-card ${v.status}`} style={{ animationDelay: i * 0.1 + 's' }}>
            <span className="vital-icon">{v.icon}</span>
            <span className="vital-label-animated">{v.label}</span>
            <span className="vital-value-animated">{v.value}</span>
            <span className="vital-unit-animated">{v.unit}</span>
            <div className="vital-pulse" />
          </div>
        ))}
      </div>
    </div>
  );
};

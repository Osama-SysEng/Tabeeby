import React, { useState, useEffect } from 'react';

export const ARLiveAssistance: React.FC<{ patientId: string; procedureId: string }> = ({ patientId, procedureId }) => {
  const [anatomyOverlay, setAnatomyOverlay] = useState<any>(null);
  useEffect(() => {
    fetch(`/api/surgical/${procedureId}/ar-overlay?patientId=${patientId}`)
      .then(r => r.json()).then(setAnatomyOverlay);
  }, [patientId, procedureId]);
  return (
    <div className="ar-live-assistance">
      <h2>مساعدة الجراحة المباشرة AR</h2>
      {anatomyOverlay && <div className="ar-overlay">{JSON.stringify(anatomyOverlay)}</div>}
      <div className="vitals-hud">
        <span>نبض: 72 bpm</span>
        <span>SpO2: 98%</span>
        <span>ضغط: 120/80</span>
      </div>
    </div>
  );
};
import React from 'react';

export const ARLiveAssistance = () => (
  <div className="ar-live">
    <h3>مساعدة الجراحة المباشرة AR</h3>
    <div className="ar-overlay">
      <h4>الطبقات التشريحية: العضلات، الأعصاب، الأوعية</h4>
      <div className="critical-points">
        <div className="cp" style={{ left: '30%', top: '45%' }}>العضو الرئيسي</div>
        <div className="cp" style={{ left: '60%', top: '30%' }}>الأوعية</div>
      </div>
    </div>
    <div className="vitals-hud">
      <span>نبض: 72 bpm</span>
      <span>SpO2: 98%</span>
      <span>ضغط: 120/80</span>
    </div>
  </div>
);

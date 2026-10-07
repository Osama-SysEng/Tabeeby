import React, { useEffect, useState } from 'react';
// تنبيهات Ultra IQ مع animation
export const AnimatedUltraIQAlerts = () => {
  const [alerts, setAlerts] = useState([
    { id: '1', type: '심박수', message: 'انخفاض ملحوظ في نبض المريض #1234', seconds: 45, confidence: 92 },
    { id: '2', type: 'السكر', message: 'مستوى السكر يرتفع بسرعة - المريض #5678', seconds: 30, confidence: 87 },
  ]);
  const [visibleCount, setVisibleCount] = useState(alerts.length);

  useEffect(() => {
    const interval = setInterval(() => {
      setVisibleCount(prev => Math.max(0, prev - 1));
      if (visibleCount === 0) {
        clearInterval(interval);
      }
    }, 1500);
    return () => clearInterval(interval);
  }, [visibleCount]);

  return (
    <div className="animated-alerts">
      <h3>تنبيهات Ultra IQ - 30-120 ثانية قبل الحدث</h3>
      <div className="alerts-container">
        {alerts.slice(0, visibleCount).map((a, i) => (
          <div key={a.id} className={`alert-slide-in alert-${i % 2 === 0 ? 'info' : 'warning'}`}>
            <div className="alert-content">
              <div className="alert-type">{a.type}</div>
              <div className="alert-message">{a.message}</div>
              <div className="alert-meta">
                <span className="seconds-counter">{a.seconds} ثانية</span>
                <span className="confidence">🎯 {a.confidence}%</span>
              </div>
            </div>
            <div className="alert-actions">
              <button className="ack-btn">تم الاعتراف</button>
              <button className="escalate-btn">تصعيد</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

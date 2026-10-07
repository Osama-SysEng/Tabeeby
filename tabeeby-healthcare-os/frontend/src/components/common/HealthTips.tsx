import React from 'react';
const tips = ['شرب 8 أكواب ماء يومياً', 'المشي 30 دقيقة يومياً', 'النوم 7-8 ساعات', 'تناول الخضار 5 حصص يومياً', 'التمارين 150 دقيقة أسبوعياً'];
export const HealthTips = () => (
  <div className="health-tips">
    <h3>نصائح صحية يومية</h3>
    {tips.map((tip, i) => <p key={i}>💡 {tip}</p>)}
  </div>
);
